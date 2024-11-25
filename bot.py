import google.generativeai as genai
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
import asyncio

# Telegram Bot Token
TELEGRAM_TOKEN = '7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo'

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY"

# Configure the Gemini API with the API Key
genai.configure(api_key=GEMINI_API_KEY)

# List of specific words for custom response
trigger_words = ['hello', 'kaha se ho', 'bolo', 'suno']

# Function to escape MarkdownV2 special characters
def escape_markdown_v2(text: str) -> str:
    return text.replace("_", "\\_").replace("*", "\\*").replace("`", "\\`").replace("[", "\\[").replace("]", "\\]").replace("(", "\\(").replace(")", "\\)").replace("~", "\\~").replace(">", "\\>").replace("#", "\\#").replace("+", "\\+").replace("-", "\\-").replace("=", "\\=").replace("|", "\\|").replace("{", "\\{").replace("}", "\\}").replace(".", "\\.").replace("!", "\\!")

async def ask_gemini(question):
    # Use the generative model from Google Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)
    
    # Return the response text
    return response.text if response.text else "Sorry, no response."


async def handle_message(client, message):
    # Get the user's message text
    user_message = message.text.lower()  # Convert to lowercase to make it case-insensitive

    # Check if the message contains any of the trigger words
    if any(trigger_word in user_message for trigger_word in trigger_words):
        reply = "Hey, I am a Google Assistant trained by Baby Music Team"
    else:
        # Simulate the typing action on Telegram (bot is typing)
        await message.chat.send_action(ChatAction.TYPING)

        # Add a short delay to simulate thinking time
        await asyncio.sleep(0.5)  # Adjust the delay as needed

        # Get response from Gemini model
        reply = await ask_gemini(user_message)

    # Apply bold formatting (for example, make 'Patna' bold)
    reply = reply.replace("Patna", "**Patna**")  # Example of making a word bold

    # Escape any special characters for MarkdownV2
    reply = escape_markdown_v2(reply)

    # Send the reply with MarkdownV2 formatting
    await message.reply_text(reply, parse_mode=ParseMode.MARKDOWN_V2)


def main():
    app = Client("gemini_bot", bot_token=TELEGRAM_TOKEN)

    # Message handler for all text messages (no need for /gemini)
    app.add_handler(filters.text & ~filters.command, handle_message)

    # Start the bot
    print("Bot is running...")
    app.run()


if __name__ == "__main__":
    main()
