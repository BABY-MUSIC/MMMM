import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import asyncio

# Telegram Bot Token
TELEGRAM_TOKEN = '7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo'

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"

# Configure the Gemini API with the API Key
genai.configure(api_key=GEMINI_API_KEY)

# List of specific words for custom response
trigger_words = ['hello', 'kaha se ho', 'bolo', 'suno']

async def ask_gemini(question):
    # Use the generative model from Google Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)
    
    # Return the response text
    return response.text if response.text else "Sorry, no response."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the user's message text
    user_message = update.message.text.lower()  # Convert to lowercase to make it case-insensitive

    # Check if the message contains any of the trigger words
    if any(trigger_word in user_message for trigger_word in trigger_words):
        reply = "Hey, I am a Google Assistant trained by Baby Music Team"
    else:
        # Simulate the typing action on Telegram (bot is typing)
        await update.message.chat.send_action(action="typing")

        # Add a short delay to simulate thinking time
        await asyncio.sleep(0.5)  # Adjust the delay as needed

        # Get response from Gemini model
        reply = await ask_gemini(user_message)

    # Send the reply
    await update.message.reply_text(reply)


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Message handler for all text messages (no need for /gemini)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
