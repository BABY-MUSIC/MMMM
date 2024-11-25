import google.generativeai as genai
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import asyncio

# Telegram Bot Token
TELEGRAM_TOKEN = '7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo'

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"

# Channel Link
CHANNEL_USERNAME = "@BABY09_WORLD"  # The username of the channel (with "@")

# Configure the Gemini API with the API Key
genai.configure(api_key=GEMINI_API_KEY)


async def ask_gemini(question):
    # Use the generative model from Google Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)
    
    # Return the response text
    return response.text if response.text else "Sorry, no response."


async def check_user_in_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        # Get the chat member status for the user in the channel
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        print(f"Chat member status: {chat_member.status}")  # Log the user's status
        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        # Log the exact error if there's an issue checking user status
        print(f"Error checking user in channel: {e}")
        return False
    return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user is a member of the channel
    is_member = await check_user_in_channel(update, context)

    if not is_member:
        # If the user is not a member, ask them to join the channel
        await update.message.reply_text(
            f"Please join the channel @BABY09_WORLD to use the bot:",
            parse_mode=ParseMode.HTML  # Change to HTML mode to avoid Markdown issues
        )
        return

    # If the user is a member, proceed with the bot's logic
    user_message = update.message.text.lower()  # Convert to lowercase to make it case-insensitive

    # Simulate typing action on Telegram (bot is typing)
    await update.message.chat.send_action(action="typing"

        # Get response from Gemini model
        reply = await ask_gemini(user_message)

    # Send the reply with Markdown parsing enabled
    await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Message handler for all text messages (no need for /gemini)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
