import requests
from telegram.ext import Updater, CommandHandler

# Telegram Bot Token
TELEGRAM_TOKEN = '7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo'

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"

# Gemini API endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + GEMINI_API_KEY


def ask_gemini(question):
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

    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        gemini_response = response.json()
        # Extracting the response text
        return gemini_response.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "Sorry, no response.")
    else:
        return "Error: Could not connect to Gemini API."


def gemini_command(update, context):
    if len(context.args) > 0:
        question = " ".join(context.args)
        reply = ask_gemini(question)
        update.message.reply_text(reply)
    else:
        update.message.reply_text("Please ask a question after /gemini command.")


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command handler for /gemini
    dispatcher.add_handler(CommandHandler("gemini", gemini_command))

    # Start the bot
    updater.start_polling()
    print("Bot is running...")
    updater.idle()


if __name__ == "__main__":
    main()
