import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Telegram Bot Token
TELEGRAM_TOKEN = '7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo'

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"

# Configure the Gemini API with the API Key
genai.configure(api_key=GEMINI_API_KEY)

async def ask_gemini(question):
    # Use the generative model from Google Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)
    
    # Return the response text
    return response.text if response.text else "Sorry, no response."


async def gemini_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        question = " ".join(context.args)

        # Simulate the typing action on Telegram (bot is typing)
        await update.message.chat.send_action(action="typing")

        # Add a short delay to simulate thinking time
        await asyncio.sleep(2)  # Adjust the delay as needed

        # Get response from Gemini model
        reply = await ask_gemini(question)

        # Send the reply
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text("Please ask a question after /gemini command.")


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handler for /gemini
    application.add_handler(CommandHandler("gemini", gemini_command))

    # Start the bot
    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
