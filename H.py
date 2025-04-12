import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 Tokens
TELEGRAM_BOT_TOKEN = "7988392037:AAFaUjcdvALKnx4EE9YmsBhdCxOK_sbcZs8"
OPENAI_API_KEY = ""

# 🧠 GPT Setup
openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = (
    "तुम एक इंसान जैसे बात करने वाले chatbot हो। जवाब बहुत छोटे, सीधे और casual होने चाहिए — "
    "जैसे कोई दोस्त WhatsApp पर बात कर रहा हो। हर सवाल का जवाब बहुत natural और friendly tone में दो। "
    "कोई लंबा explanation नहीं देना है। जवाब में कभी-कभी emoji भी use कर सकते हो।"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("हाय! मैं एक दोस्ताना चैटबॉट हूँ 😊 मुझसे कुछ भी पूछो।")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    # GPT-4 से जवाब लेना
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ]
    )

    reply = response.choices[0].message.content.strip()
    await update.message.reply_text(reply)

# 📦 Main Bot Function
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
