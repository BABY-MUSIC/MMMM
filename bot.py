from telegram import Update, ChatMember, ChatMemberStatus
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import google.generativeai as genai
import asyncio

# Telegram Bot Token
TELEGRAM_TOKEN = '7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo'

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"

# Channel username
CHANNEL_USERNAME = "@BABY09_WORLD"

# Configure the Gemini API with the API Key
genai.configure(api_key=GEMINI_API_KEY)

async def ask_gemini(question):
    # Use the generative model from Google Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)
    
    # Return the response text
    return response.text if response.text else "Sorry, no response."


async def is_user_in_channel(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    """
    Check if the user is a member of the specified channel.
    """
    try:
        member_status = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member_status.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        print(f"Error checking channel membership: {e}")
        return False


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the user's ID
    user_id = update.effective_user.id

    # Check if the user is a member of the channel
    if not await is_user_in_channel(context, user_id):
        # Notify the user to join the channel
        await update.message.reply_text(
            f"⚠️ To use this bot, please first join our channel: {CHANNEL_USERNAME}"
        )
        return

    # Get the user's message text
    user_message = update.message.text.lower()  # Convert to lowercase to make it case-insensitive

    # Simulate typing action on Telegram (bot is typing)
    await update.message.chat.send_action(action="typing")

    # Add a short delay to simulate thinking time
    await asyncio.sleep(0.5)  # Adjust the delay as needed

    # Get response from Gemini model
    reply = await ask_gemini(user_message)

    # Send the reply with Markdown parsing enabled
    await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Message handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
