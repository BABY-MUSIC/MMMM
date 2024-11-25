import asyncio
import logging
from typing import Dict

import google.generativeai as genai
from pymongo import MongoClient
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters, ContextTypes, 1  CommandHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TELEGRAM_TOKEN = '7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo'

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"

# Channel Link
CHANNEL_USERNAME = "@BABY09_WORLD"  # The username of the channel (with "@")

# Owner ID
OWNER_ID = 7400383704

# MongoDB Connection
MONGO_URI = "mongodb+srv://Yash_607:Yash_607@cluster0.r3s9sbo.mongodb.net/?retryWrites=true&w=majority/"  # Replace with your MongoDB connection string
DATABASE_NAME = "telegram_bot"
COLLECTION_NAME = "authorized_users"

# Configure the Gemini API 
genai.configure(api_key=GEMINI_API_KEY)

# Cache to store recent responses
response_cache = {}  

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
authorized_users_collection = db[COLLECTION_NAME]


async def ask_gemini(question):
    # Check if the response is in the cache
    if question in response_cache:
        return response_cache[question]

    # Use the generative model from Google Gemini (try a smaller model if available)
    model = genai.GenerativeModel("gemini-1.5-flash") 
    response = model.generate_content(question, max_tokens=512) # Adjust max_tokens as needed

    # Return the response text
    reply = response.text if response.text else "Sorry, no response."

    # Store the response in the cache
    response_cache[question] = reply 
    return reply


async def is_authorized(user_id: int):
    """Checks if a user is authorized to use the bot."""
    user = authorized_users_collection.find_one({"user_id": user_id})
    return user is not None


async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Approves a user to use the bot."""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("You are not authorized to approve users.")
        return

    try:
        username = context.args[0]  # Get the username from the command arguments
        user = await context.bot.get_chat(username)  # Get user details from Telegram
        user_id = user.id

        # Store the authorized user in MongoDB
        authorized_users_collection.insert_one({"user_id": user_id, "username": username})

        await update.message.reply_text(f"User {username} has been approved!")
    except IndexError:
        await update.message.reply_text("Please provide a username to approve. Usage: `/approve @username`")
    except Exception as e:
        logger.error(f"Error approving user: {e}")
        await update.message.reply_text("An error occurred while approving the user.")


async def check_user_in_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        # Get the chat member status for the user in the channel
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        print(f"Chat member status: {chat_member.status}")  # Log the user's status
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        # Log the exact error if there's an issue checking user status
        print(f"Error checking user in channel: {e}")
        return False


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_authorized(user_id):
        await update.message.reply_text(
            "You are not authorized to use this bot. Please contact the bot owner for approval."
        )
        return

    is_member = await check_user_in_channel(update, context)

    if not is_member:
        await update.message.reply_text(
            f"Please join the channel {CHANNEL_USERNAME} to use the bot:",
            parse_mode=ParseMode.HTML
        )
        return

    user_message = update.message.text.lower()

    # Combine typing action and response
    reply = await ask_gemini(user_message)
    await update.message.reply_text(
        f"_{reply}_",  # Include reply within Markdown for italics
        parse_mode=ParseMode.MARKDOWN
    ) 


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handler for /approve
    application.add_handler(CommandHandler("approve", approve_user))

    # Message handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
