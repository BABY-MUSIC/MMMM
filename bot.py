import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Telegram Bot Token
TELEGRAM_TOKEN = '7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo'

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"

# Gemini API endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + GEMINI_API_KEY


async def ask_gemini(question):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }
    
    # Use aiohttp to make async HTTP request
    async with aiohttp.ClientSession() as session:
        async with session.post(GEMINI_API_URL, headers=headers, json=data) as response:
            if response.status == 200:
                gemini_response = await response.json()
                return gemini_response.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "Sorry, no response.")
            else:
                return "Error: Could not connect to Gemini API."


async def gemini_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        question = " ".join(context.args)
        reply = await ask_gemini(question)
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
