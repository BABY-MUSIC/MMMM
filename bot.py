import asyncio
import random
import re
import logging
import os
from pyrogram.enums import ChatAction
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from flask import Flask
from threading import Thread
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


# Set up logging to track errors and bot activity
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# MongoDB setup (using motor for async access)
MONGO_URL = "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority"
mongo_client = AsyncIOMotorClient(MONGO_URL)
word_db = mongo_client["Word"]["WordDb"]  # Collection for word-response pairs

# Bot configuration
API_ID = "16457832"  # Replace with your API ID
API_HASH = "3030874d0befdb5d05597deacc3e83ab"  # Replace with your API Hash
BOT_TOKEN = "7645090253:AAFPA_HC1oTDWt9z4sRWcfP6BU_IeaY3-Z0"  # Replace with your Bot Token

# Initialize bot client
RADHIKA = Client(
    "my_bot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN
)

# Regular expression to filter unwanted messages
UNWANTED_MESSAGE_REGEX = r"^[\W_]+$|[\/!?\~\\]"

# Channel ID or message link to forward from
CHANNEL_ID = "RadhikaCommunity"  # Channel username (without '@')
MESSAGE_ID = 2354  # Message ID to forward

# /start command to forward a specific message from the channel
# Define the owner's Telegram user ID
OWNER_ID = 6657539971  # Replace with the actual owner ID

@RADHIKA.on_message(filters.command(["clone"], prefixes="/") | filters.regex(r"(?i)\bclone\b"))
async def handle_clone(client, message):
    await message.reply(
        "Currently unavailable. Contact Support chat [here](https://t.me/+HiS0W_Zz2XJhNjZl)",
        disable_web_page_preview=True
    )

# प्लान बटन बनाने के लिए
PLANS = {
    "50": "1 Hour",
    "100": "6 Hours",
    "200": "24 Hours",
    "500": "3 Days"
}


import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup,
    InlineKeyboardButton, Message
)




@RADHIKA.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    if len(message.command) > 1 and message.command[1] == "call":
        buttons = [[f"₹{price} for {duration}"] for price, duration in PLANS.items()]
        
        sent_msg = await message.reply_text(
            "Please choose your plan:",
            reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
        )
        
        try:
            # ✅ User का अगला मैसेज कैप्चर करने के लिए wait_for_message() का उपयोग
            response = await client.wait_for_message(
                chat_id=message.chat.id,
                filters=filters.text,
                timeout=60
            )

            if response.text in [f"₹{price} for {duration}" for price, duration in PLANS.items()]:
                price = response.text.split(" ")[0][1:]  # ₹ हटाकर प्राइस निकालना
                
                # 🔄 Processing Message
                processing_msg = await response.reply_text("Processing...")
                await asyncio.sleep(2)
                await processing_msg.delete()

                # 📸 Plan Image + Check Button
                image_path = f"plans/{price}.png"  # इमेज का पाथ
                
                try:
                    await client.send_photo(
                        chat_id=message.chat.id,
                        photo=image_path,
                        caption=f"**✅ Plan Selected: ₹{price} for {PLANS[price]}**",
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("✅ Check", callback_data=f"check_{price}")]]
                        )
                    )
                except Exception as e:
                    await response.reply_text(f"Error loading plan image: {e}")

        except asyncio.TimeoutError:
            await sent_msg.reply_text("❌ No response received. Try again.", reply_markup=ReplyKeyboardRemove())
    
        return  # ताकि chatbot handler इसको प्रोसेस न करे

    # ✅ Default Reply (Forward Message)
    try:
        await client.forward_messages(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_ids=MESSAGE_ID
        )
    except Exception as e:
        await message.reply_text("Something went wrong while forwarding the message.")

# ✅ Check बटन पर क्लिक करने पर पॉपअप मैसेज
@RADHIKA.on_callback_query(filters.regex(r"^check_\d+$"))
async def check_plan(client: Client, query):
    await query.answer("Thanks for choosing the plan!", show_alert=True)




# Combined responder for both group and private chats
@RADHIKA.on_message(filters.all & ~filters.bot)
async def chatbot_handler(client, message: Message):
    if message.text:  # Only handle messages with text
        logger.info(f"Received message: {message.text} (Chat ID: {message.chat.id}, Private: {message.chat.type == 'private'})")
        
        # Ignore unwanted messages
        if re.match(UNWANTED_MESSAGE_REGEX, message.text):
            logger.info("Unwanted message (special characters). Ignored.")
            return

        # Send typing action in private and group chats
        if message.chat.type in ["private", "group"]:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if not message.reply_to_message:  # If not a reply
            responses = await word_db.find({"word": message.text}).to_list(length=10)
            if responses:
                response = random.choice(responses)
                try:
                    if response["check"] == "sticker":
                        await message.reply_sticker(response["text"])
                    else:
                        await message.reply_text(response["text"])
                except Exception as e:
                    logger.error(f"Error sending response: {e}")
        else:  # If it's a reply
            reply = message.reply_to_message
            if reply.from_user.id == (await client.get_me()).id:  # If replying to bot's message
                responses = await word_db.find({"word": message.text}).to_list(length=10)
                if responses:
                    response = random.choice(responses)
                    try:
                        if response["check"] == "sticker":
                            await message.reply_sticker(response["text"])
                        else:
                            await message.reply_text(response["text"])
                    except Exception as e:
                        logger.error(f"Error sending response: {e}")
            else:  # If replying to a user's message
                if message.text:
                    await word_db.insert_one({"word": reply.text, "text": message.text, "check": "text"})
                elif message.sticker:
                    await word_db.insert_one({"word": reply.text, "text": message.sticker.file_id, "check": "sticker"})
                logger.info("Learned new word-response pair.")

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Flask app is running!"

# Run Flask app in a separate thread to not block the bot's execution
def run_flask():
    port = int(os.environ.get("PORT", 8000))  # Get the port from environment variable or use 8000 as fallback
    app.run(host='0.0.0.0', port=port, debug=False)

# Run the bot client and Flask in separate threads
if __name__ == "__main__":
    # Start Flask app in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Start the Pyrogram bot and keep it running
    try:
        logger.info("Starting bot...")
        # Start the bot client
        RADHIKA.run()

        # Keep the bot alive by calling idle()
        asyncio.run(RADHIKA.idle())
    except Exception as e:
        logger.error(f"Error running the bot: {e}")
