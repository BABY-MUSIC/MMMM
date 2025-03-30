import os
import yt_dlp
import googleapiclient.discovery
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup

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

# 🔹 yt-dlp से YouTube वीडियो को MP3 में डाउनलोड करना
def download_audio(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    file_name = f"{video_id}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_name,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return file_name
    except Exception as e:
        print(f"⚠️ Download Error: {e}")
        return None

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
