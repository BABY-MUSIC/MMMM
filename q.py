import asyncio
import logging
import os
from pyrogram import Client, filters
from pyrogram.types import Message

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

API_ID = "16457832"
API_HASH = "3030874d0befdb5d05597deacc3e83ab"
BOT_TOKEN = "7242058454:AAE6TakbWWxpS6Xiq-XLXpWPZew9wzxNAu8"

RADHIKA = Client(
    "my_bot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN
)

CHANNEL_ID = "yudffja"
MESSAGE_ID = 3
OWNER_ID = 6657539971

@RADHIKA.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    # ✅ Owner को Notify करना
    user_mention = message.from_user.mention
    user_id = message.from_user.id
    
    notify_text = f"👤 **New User Started Bot**\n\n🔹 **User:** {user_mention} (`{user_id}`)\n🔹 **Chat ID:** `{message.chat.id}`"
    
    try:
        await client.send_message(OWNER_ID, notify_text)
    except Exception as e:
        logger.error(f"Failed to notify owner: {e}")
    
    try:
        await client.forward_messages(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_ids=MESSAGE_ID
        )
    except Exception as e:
        await message.reply_text("Something went wrong while forwarding the message.")

if __name__ == "__main__":
    try:
        logger.info("Radhika started...")
        RADHIKA.run()
    except Exception as e:
        logger.error(f"Error running the bot: {e}")
