import os
import requests
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
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

# 🔹 yt5s.io से YouTube वीडियो का MP3 लिंक पाना (बिना Login)
def get_direct_mp3_link(video_id):
    try:
        url = f"https://yt5s.io/api/ajaxSearch"
        data = {"q": f"https://www.youtube.com/watch?v={video_id}", "vt": "mp3"}
        response = requests.post(url, data=data).json()
        
        if "links" in response:
            return response["links"]["mp3"]["link"]
    except Exception as e:
        print(f"⚠️ Download Link Error: {e}")
    
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
    
    keyboard = [[title] for title, video_id in results]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    message.reply_text("🔍 टॉप 10 गाने:", reply_markup=reply_markup)

# 🔹 जब कोई गाना चुने तो डाउनलोड और भेजें
@bot.on_message(filters.text)
def song_download(client, message):
    query = message.text
    results = search_youtube(query)
    
    for title, video_id in results:
        if title == query:
            message.reply_text("📥 डाउनलोड हो रहा है...")
            file_path = download_audio(video_id)
            
            if file_path:
                message.reply_audio(file_path, title=title)
                os.remove(file_path)
            else:
                message.reply_text("❌ डाउनलोड लिंक नहीं मिला!")
            return
    
    message.reply_text("❌ कृपया सही विकल्प चुनें!")

# 🔹 बॉट रन करें
bot.run()
