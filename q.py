import os
import requests
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import googleapiclient.discovery

# 🔹 Bot Credentials
BOT_TOKEN = "8052771146:AAEZGJamIo3pfcNe_q3WpTOIYHRFEL8Jpp8"
API_ID = "16457832"
API_HASH = "3030874d0befdb5d05597deacc3e83ab"
YOUTUBE_API_KEY = "AIzaSyDv7VX5N_BTBHksa3QI4LFuWXE_AZH-eT4"

# 🔹 Pyrogram Client
bot = Client("music_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# 🔹 YouTube से टॉप 10 गाने खोजना

def search_youtube(query):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(q=query, part="snippet", type="video", maxResults=10)
    response = request.execute()
    
    results = []
    for video in response.get("items", []):
        title = video["snippet"]["title"]
        video_id = video["id"]["videoId"]
        results.append((title, video_id))
    
    return results

# 🔹 Invidious API से MP3 लिंक पाना

def get_direct_mp3_link(video_id):
    try:
        url = f"https://api.invidious.io/api/v1/videos/{video_id}"
        response = requests.get(url).json()

        if "adaptiveFormats" in response:
            for fmt in response["adaptiveFormats"]:
                if "audio" in fmt["type"]:
                    return fmt["url"]
    except Exception as e:
        print(f"⚠️ Error: {e}")
    
    return None

# 🔹 डाउनलोड और भेजने का प्रोसेस
def download_audio(video_id):
    mp3_link = get_direct_mp3_link(video_id)
    if not mp3_link:
        return None

    file_name = f"{video_id}.mp3"
    response = requests.get(mp3_link, stream=True)

    with open(file_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    
    return file_name

# 🔹 /song कमांड पर टॉप 10 गाने दिखाना
@bot.on_message(filters.command("song"))
def song_search(client, message):
    query = message.text.replace("/song ", "")
    results = search_youtube(query)
    
    if not results:
        message.reply_text("❌ कोई गाना नहीं मिला!")
        return
    
    keyboard = [[InlineKeyboardButton(title, callback_data=video_id)] for title, video_id in results]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message.reply_text("🎵 नीचे से कोई गाना चुनें:", reply_markup=reply_markup)

# 🔹 जब कोई गाना चुने तो डाउनलोड और भेजें
@bot.on_callback_query()
def song_download(client, callback_query):
    video_id = callback_query.data
    callback_query.message.edit_text("📥 डाउनलोड हो रहा है...")
    
    file_path = download_audio(video_id)
    if file_path:
        callback_query.message.reply_audio(file_path, title="Downloaded Song")
        os.remove(file_path)
    else:
        callback_query.message.edit_text("❌ डाउनलोड लिंक नहीं मिला!")

# 🔹 बॉट रन करें
bot.run()
