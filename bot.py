from telegram.ext import Updater, CommandHandler
import google.generativeai as genai

# Configure Gemini API
API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"
genai.configure(api_key=API_KEY)
model_name = "gemini-1.5-flash"

# Function to handle /gemini command
def gemini(update, context):
    if len(context.args) == 0:
        update.message.reply_text("कृपया /gemini के बाद एक प्रश्न प्रदान करें।")
        return

    user_question = " ".join(context.args)

    try:
        # Generate response using Gemini API
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(user_question)

        # Send the Gemini response to the user
        if response and hasattr(response, "text"):
            update.message.reply_text(response.text)
        else:
            update.message.reply_text("मुझे Gemini से प्रतिक्रिया प्राप्त करने में समस्या हुई।")

    except Exception as e:
        # Handle errors
        update.message.reply_text(f"Gemini API के साथ कनेक्शन में समस्या: {str(e)}")

# Main function to start the bot
def main():
    # Replace YOUR_TELEGRAM_BOT_TOKEN with your bot token
    updater = Updater("7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo", use_context=True)
    dp = updater.dispatcher

    # Add command handler for /gemini
    dp.add_handler(CommandHandler("gemini", gemini))

    # Start the bot
    updater.start_polling()
    updater.idle()

if name == "main":
    main()
