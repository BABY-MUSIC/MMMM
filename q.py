from telethon import TelegramClient, events
import asyncio

# अपनी API ID और HASH यहाँ डालें
API_ID = 16457832  # अपना API ID डालें
API_HASH = "3030874d0befdb5d05597deacc3e83ab"
BOT_TOKEN = "8108105726:AAEytIK1fGJTK7YdKQG6nJZxjLgL-OABGRA"

client = TelegramClient("quiz_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage)
async def quiz_solver(event):
    # अगर यह पोल है और क्विज मोड में है
    if event.poll and event.poll.quiz:
        correct_option = None

        # सही उत्तर का index खोजें
        for i, option in enumerate(event.poll.answers):
            if option.correct:
                correct_option = i
                break

        if correct_option is not None:
            # सही उत्तर भेजें
            await event.respond(f"/vote {correct_option}")
            await asyncio.sleep(2)  # कुछ सेकंड रुके ताकि स्पैम न लगे

client.run_until_disconnected()
