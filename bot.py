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
GEMINI_API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"

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
    response = model.generate_content(question, max_tokens=512)

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
    # ... (no changes in this function)


async def check_user_in_channel(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    # ... (no changes in this function)


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

    # ... (no changes in main function)


if __name__ == "__main__":
    main()
