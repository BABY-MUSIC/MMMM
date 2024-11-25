import asyncio
import logging
from typing import Dict

import google.generativeai as genai
from pymongo import MongoClient
from telegram import Update, error
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
    CommandHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TELEGRAM_TOKEN = "7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo" 

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"  # Replace with your actual Gemini API key

# Channel Link
CHANNEL_USERNAME = "@BABY09_WORLD"

# Owner ID
OWNER_ID = 7400383704

# MongoDB Connection
MONGO_URI = "mongodb+srv://Yash_607:Yash_607@cluster0.r3s9sbo.mongodb.net/?retryWrites=true&w=majority"
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

    # Use the generative model from Google Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)  # Removed max_tokens

    # Return the response text
    reply = response.text if response.text else "Sorry, no response."

    # Store the response in the cache
    response_cache[question] = reply
    return reply


async def is_authorized(user_id: int):
    """Checks if a user is authorized to use the bot."""
    # Automatically authorize the owner
    if user_id == OWNER_ID:
        return True
    user = authorized_users_collection.find_one({"user_id": user_id})
    return user is not None


async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Approves a user to use the bot."""
    logger.info("Approve user command received.")

    if update.effective_user.id != OWNER_ID:
        logger.warning(
            f"Unauthorized user tried to approve: {update.effective_user.id}"
        )
        await update.message.reply_text("You are not authorized to approve users.")
        return

    try:
        username = context.args[0]
        try:
            user = await context.bot.get_chat(username)
            user_id = user.id

            # Store the authorized user in MongoDB
            authorized_users_collection.insert_one({
                "user_id": user_id,
                "username": username
            })

            await update.message.reply_text(f"User {username} has been approved!")
        except error.TelegramError as e:
            logger.error(f"Error getting user chat: {e}")
            await update.message.reply_text(
                "Error getting user information. Please check the username.")
            return

    except IndexError:
        await update.message.reply_text(
            "Please provide a username to approve. Usage: `/approve @username`"
        )
    except Exception as e:
        logger.exception(f"Error approving user: {e}")
        await update.message.reply_text(
            "An error occurred while approving the user.")


async def check_user_in_channel(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME,
                                                        user_id)
        logger.info(f"Chat member status: {chat_member.status}")
        return chat_member.status in ["member", "administrator", "creator"]
    except error.TelegramError as e:
        logger.error(f"Error checking user in channel: {e}")
        return False


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check authorization AND channel membership
    authorized = await is_authorized(user_id)
    member_of_channel = await check_user_in_channel(update, context)

    if not authorized:
        await update.message.reply_text(
            "You are not authorized to use this bot. Please contact the bot owner for approval."
        )
        return

    if not member_of_channel:
        await update.message.reply_text(
            f"Please join the channel {CHANNEL_USERNAME} to use the bot:",
            parse_mode=ParseMode.HTML,
        )
        return

    user_message = update.message.text.lower()

    # Get the response from Gemini
    reply = await ask_gemini(user_message)

    # Combine typing action and response
    await update.message.reply_text(f"_{reply}_",
                                    parse_mode=ParseMode.MARKDOWN)


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handler for /approve
    application.add_handler(CommandHandler("approve", approve_user))

    # Message handler for all text messages
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
