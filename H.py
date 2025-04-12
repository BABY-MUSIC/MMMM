import openai
import logging
from pyrogram import Client, filters

# ✅ Setup logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# 🚫 SECURITY NOTE: Replace these with environment variables in production
API_ID = "16457832"  # Replace with your actual API ID
API_HASH = "3030874d0befdb5d05597deacc3e83ab"  # Replace with your actual API Hash
TELEGRAM_BOT_TOKEN = "7988392037:AAFaUjcdvALKnx4EE9YmsBhdCxOK_sbcZs8"  # Replace with your actual bot token
OPENAI_API_KEY = ""  # Replace with your actual OpenAI API key

# 🔐 OpenAI API key
openai.api_key = OPENAI_API_KEY

# 🧠 ChatGPT Prompt for natural, human-like replies
SYSTEM_PROMPT = (
    "तुम एक इंसान जैसे बात करने वाले chatbot हो। जवाब बहुत छोटे, सीधे और casual होने चाहिए — "
    "जैसे कोई दोस्त WhatsApp पर बात कर रहा हो। हर सवाल का जवाब बहुत natural और friendly tone में दो। "
    "कोई लंबा explanation नहीं देना है। जवाब में कभी-कभी emoji भी use कर सकते हो।"
)

# 🟢 Start Command Handler
async def start(client, message):
    await message.reply_text("हाय! मैं एक दोस्ताना चैटबॉट हूँ 😊 मुझसे कुछ भी पूछो।")

# 💬 Message Handler for user messages
async def handle_message(client, message):
    user_msg = message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Updated to GPT-4
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ]
        )

        reply = response.choices[0].message["content"].strip()  # Correct response format
        await message.reply_text(reply)

    except Exception as e:
        logging.error(f"OpenAI Error: {e}")
        await message.reply_text("सॉरी, कुछ गड़बड़ हो गई 😅 बाद में ट्राय करें।")

# 🔁 Main bot runner
app = Client(
    "chatbot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=TELEGRAM_BOT_TOKEN
)

# Add handlers using decorators
@app.on_message(filters.command("start"))
async def on_start(client, message):
    await start(client, message)

@app.on_message(filters.text & ~filters.command(""))
async def on_message(client, message):
    await handle_message(client, message)

# Start the bot
if __name__ == "__main__":
    print("🤖 Bot is running...")
    app.run()
