import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from io import BytesIO

# Configure Google Generative AI
genai.configure(api_key=os.environ['AIzaSyDq47CQUgrNXQ5WCgw9XDJCudlUrhyC-pY'])
imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")

# Define the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Send me a text prompt, and I will generate an image for you."
    )

# Define the image generation handler
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    try:
        # Generate images
        result = imagen.generate_images(
            prompt=prompt,
            number_of_images=1,  # Generate one image for simplicity
            safety_filter_level="block_only_high",
            person_generation="allow_adult",
            aspect_ratio="3:4",
        )

        # Convert the image to a file and send to the user
        for image in result.images:
            image_data = BytesIO()
            image._pil_image.save(image_data, format="PNG")
            image_data.seek(0)
            await update.message.reply_photo(photo=image_data, caption=f"Image for: {prompt}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Main function to run the bot
def main():
    telegram_token = os.environ['7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo']  # Set your Telegram Bot Token in the environment variable
    application = ApplicationBuilder().token(telegram_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
