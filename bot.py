import google.generativeai as genai
from telegram import Update, ChatAction
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import asyncio

# Telegram Bot Token
TELEGRAM_TOKEN = '7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo'

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"

# Channel Link
CHANNEL_USERNAME = "@BABY09_WORLD"  # Ensure this starts with '@'

# Configure the Gemini API with the API Key
genai.configure(api_key=GEMINI_API_KEY)

async def ask_gemini(question):
    try:
        response = genai.generate_text(prompt=question)
        # Return the first generated response
        return response.candidates[0]['content'] if response.candidates else "Sorry, no response."
    except Exception as e:
        print(f"Error in Gemini API call: {e}")
        return "Sorry, I couldn't process your request."

async def check_user_in_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        # Get the chat member status for the user in the channel
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        # Log the error for debugging
        print(f"Error checking user in channel: {e}")
        
        # Provide user-friendly debug messages
        if "chat not found" in str(e).lower():
            print("Bot might not be added to the channel or the username is incorrect.")
        elif "user not found" in str(e).lower():
            print("The user may not exist or privacy settings might block access.")
        else:
            print("An unexpected error occurred.")
    return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user is a member of the channel
    is_member = await check_user_in_channel(update, context)

    if not is_member:
        # If the user is not a member, ask them to join the channel
        await update.message.reply_text(
            f"Please join the channel {CHANNEL_USERNAME} to use the bot.",
            parse_mode=ParseMode.HTML  # Use HTML parsing
        )
        return

    # If the user is a member, proceed with the bot's logic
    user_message = update.message.text.lower()  # Convert to lowercase for case-insensitivity

    # Simulate typing action on Telegram
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

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
