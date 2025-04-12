import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from pyrogram import Client, filters

# Logging
logging.basicConfig(level=logging.INFO)

# Telegram Bot Config
API_ID = 16457832  # अपने वाले डाल
API_HASH = "3030874d0befdb5d05597deacc3e83ab"
BOT_TOKEN = "7988392037:AAFaUjcdvALKnx4EE9YmsBhdCxOK_sbcZs8"

# Hugging Face model config
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")

SYSTEM_PROMPT = (
    "तुम एक इंसान जैसे बात करने वाले chatbot हो। जवाब बहुत छोटे, सीधे और casual होने चाहिए — "
    "जैसे कोई दोस्त WhatsApp पर बात कर रहा हो। हर सवाल का जवाब बहुत natural और friendly tone में दो। "
    "कोई लंबा explanation नहीं देना है। जवाब में कभी-कभी emoji भी use कर सकते हो।"
)

# Telegram Bot Setup
app = Client("babybot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start Message
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("हाय! मैं तेरा बेबी-बॉट हूँ, बोलो क्या हाल है?")

# Chat Handler
@app.on_message(filters.text & ~filters.command(""))
async def reply(client, message):
    user_msg = message.text

    prompt = f"{SYSTEM_PROMPT}\nUser: {user_msg}\nBot:"

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_new_tokens=150, do_sample=True, temperature=0.7)
    reply_text = tokenizer.decode(output[0], skip_special_tokens=True)
    reply_text = reply_text.split("Bot:")[-1].strip()

    await message.reply_text(reply_text)

# Run
if __name__ == "__main__":
    print("🤖 BabyBot is running...")
    app.run()
