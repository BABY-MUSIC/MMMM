import random
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient

# MongoDB setup
MONGO_URL = "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority"
mongo_client = MongoClient(MONGO_URL)
word_db = mongo_client["Word"]["WordDb"]  # Stores word-response pairs

# Initialize bot client
API_ID = "16457832"  # Replace with your API ID
API_HASH = "3030874d0befdb5d05597deacc3e83ab"  # 3030874d0befdb5d05597deacc3e83ab with your API Hash
BOT_TOKEN = "7561329328:AAH33CSzIkYLsFAqjJe_e_H0leDz9H6iOEU"  # Replace with your Bot Token

# Initialize bot client with API ID, API hash, and bot token
RADHIKA = Client(
    "my_bot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN
)


# Regular expression to filter unwanted messages
UNWANTED_MESSAGE_REGEX = r"^[\W_]+$|[\/!?\~\\]"

# Channel ID or message link to forward from
CHANNEL_ID = "II_DUNIYA_0"  # Channel username (without '@')
MESSAGE_ID = 3510  # Message ID to forward

# /start command to forward a specific message from a channel
@RADHIKA.on_message(filters.command("start", prefixes=["/"]))
async def start(client, message: Message):
    try:
        # Forwarding the specific message from the channel
        await message.forward(CHANNEL_ID, message_id=MESSAGE_ID)
        await message.reply_text("Here's the post you requested!")
    except Exception as e:
        print(f"Error forwarding message: {e}")
        await message.reply_text("Something went wrong while forwarding the message.")

# Regular responder to messages in group or private chats
@RADHIKA.on_message((filters.text | filters.sticker) & ~filters.private & ~filters.bot)
async def chatbot_responder(client, message: Message):
    if message.text and re.match(UNWANTED_MESSAGE_REGEX, message.text):
        return
    
    if message.text:
        responses = list(word_db.find({"word": message.text}))
        if responses:
            response = random.choice(responses)
            try:
                if response["check"] == "sticker":
                    await message.reply_sticker(response["text"])
                else:
                    await message.reply_text(response["text"])
            except Exception as e:
                print(f"Error sending response: {e}")

# Regular responder for private chats
@RADHIKA.on_message((filters.text | filters.sticker) & filters.private & ~filters.bot)
async def chatbot_private(client, message: Message):
    if message.text and re.match(UNWANTED_MESSAGE_REGEX, message.text):
        return
    
    await RADHIKA.send_chat_action(message.chat.id, "typing")

    if not message.reply_to_message:
        responses = list(word_db.find({"word": message.text}))
        if responses:
            response = random.choice(responses)
            try:
                if response["check"] == "sticker":
                    await message.reply_sticker(response["text"])
                else:
                    await message.reply_text(response["text"])
            except Exception as e:
                print(f"Error sending response: {e}")
    else:
        reply = message.reply_to_message
        if reply.from_user.id == (await RADHIKA.get_me()).id:
            responses = list(word_db.find({"word": message.text}))
            if responses:
                response = random.choice(responses)
                try:
                    if response["check"] == "sticker":
                        await message.reply_sticker(response["text"])
                    else:
                        await message.reply_text(response["text"])
                except Exception as e:
                    print(f"Error sending response: {e}")
        else:
            if message.text:
                word_db.insert_one({"word": reply.text, "text": message.text, "check": "text"})
            elif message.sticker:
                word_db.insert_one({"word": reply.text, "text": message.sticker.file_id, "check": "sticker"})

# Run the bot
RADHIKA.run()
