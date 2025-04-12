import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import logging

# ✅ Setup logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# 🚫 SECURITY NOTE: Replace these with environment variables in production
TELEGRAM_BOT_TOKEN = "7988392037:AAFaUjcdvALKnx4EE9YmsBhdCxOK_sbcZs8"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# 🔐 OpenAI API key
openai.api_key = OPENAI_API_KEY

# 🧠 ChatGPT Prompt for natural, human-like replies
SYSTEM_PROMPT = (
    "तुम एक इंसान जैसे बात करने वाले chatbot हो। जवाब बहुत छोटे, सीधे और casual होने चाहिए — "
    "जैसे कोई दोस्त WhatsApp पर बात कर रहा हो। हर सवाल का जवाब बहुत natural और friendly tone में दो। "
    "कोई लंबा explanation नहीं देना है। जवाब में कभी-कभी emoji भी use कर सकते हो।"
)

# 🟢 Start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("हाय! मैं एक दोस्ताना चैटबॉट हूँ 😊 मुझसे कुछ भी पूछो।")

# 💬 Message Handler for user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # या "gpt-4" अगर आपके पास एक्सेस है
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ]
        )

        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"OpenAI Error: {e}")
        await update.message.reply_text("सॉरी, कुछ गड़बड़ हो गई 😅 बाद में ट्राय करें।")

# 🔁 Main bot runner
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
