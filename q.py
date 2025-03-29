import os
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
import googleapiclient.discovery

# 🔹 API Keys
BOT_TOKEN = "8052771146:AAEZGJamIo3pfcNe_q3WpTOIYHRFEL8Jpp8"
API_ID = "16457832"
API_HASH = "3030874d0befdb5d05597deacc3e83ab"
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

# 🔹 Pyrogram Client
bot = Client("music_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# 🔹 YouTube Search Function
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

# 🔹 Download YouTube Audio
def download_audio(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    options = {
        "format": "bestaudio/best",
        "outtmpl": f"{video_id}.mp3",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    return f"{video_id}.mp3"

# 🔹 Handle Song Search
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

# 🔹 Handle Song Selection
@bot.on_message(filters.text)
def song_download(client, message):
    query = message.text
    results = search_youtube(query)
    
    for title, video_id in results:
        if title == query:
            message.reply_text("📥 डाउनलोड हो रहा है...")
            file_path = download_audio(video_id)
            message.reply_audio(file_path, title=title)
            os.remove(file_path)
            return
    
    message.reply_text("❌ कृपया सही विकल्प चुनें!")

# 🔹 Run Bot
bot.run()
