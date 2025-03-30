import os
import yt_dlp
import requests
from flask import Flask, request, jsonify, send_file
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔹 Telegram Bot Credentials
BOT_TOKEN = "8052771146:AAEZGJamIo3pfcNe_q3WpTOIYHRFEL8Jpp8"
API_ID = "16457832"
API_HASH = "3030874d0befdb5d05597deacc3e83ab"

# 🔹 Flask API Setup
app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# 🔹 YouTube Search Function
def youtube_search(query):
    ydl_opts = {"quiet": True, "default_search": "ytsearch10", "extract_flat": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
        return result.get("entries", [])

# 🔹 MP3 Download Function
@app.route('/download', methods=['GET'])
def download_audio():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

    return jsonify({"file_path": filename})

@app.route('/file/<filename>', methods=['GET'])
def get_file(filename):
    return send_file(f"{DOWNLOAD_FOLDER}/{filename}", as_attachment=True)

# 🔹 Run Flask API in a Thread
def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False)

Thread(target=run_flask).start()

# 🔹 Start Telegram Bot
bot = Client("ytmp3_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("song") & filters.private)
async def search_song(_, message):
    if len(message.command) < 2:
        await message.reply("🎵 कृपया गाने का नाम भेजें।\nउदाहरण: `/song Tum Hi Ho`")
        return

    query = " ".join(message.command[1:])
    results = youtube_search(query)

    if not results:
        await message.reply("❌ कोई गाना नहीं मिला!")
        return

    buttons = [[InlineKeyboardButton(f"{idx+1}. {result['title']}", callback_data=f"download_{result['url']}")] for idx, result in enumerate(results[:10])]

    await message.reply("🎶 **चुनें कोई गाना:**", reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex(r"^download_(.+)"))
async def download_selected_song(_, query):
    url = query.data.split("_")[1]

    await query.message.edit("⏳ गाना डाउनलोड हो रहा है...")

    response = requests.get(f"http://127.0.0.1:5000/download", params={"url": url}).json()

    if "file_path" in response:
        filename = response["file_path"]
        await query.message.reply_audio(audio=filename, caption="🎵 आपका गाना!")
    else:
        await query.message.edit("⚠ कोई समस्या हुई, कृपया पुनः प्रयास करें।")

bot.run()
