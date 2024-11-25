import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from io import BytesIO

# Configure Google Generative AI
genai.configure(api_key=os.getenv('API_KEY', '7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo'))

def get_image_generation_model():
    """Retrieve an image generation model from the available list of models."""
    try:
        models = genai.list_models()
        for model in models:
            if "image" in model.name.lower():
                print(f"Selected Model: {model.name}")
                return model.name
        print("No suitable image generation model found.")
        return None
    except Exception as e:
        print(f"Error retrieving models: {e}")
        return None

# Dynamically select an image generation model
MODEL_NAME = get_image_generation_model()

# Define the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Send me a text prompt, and I will generate an image for you (if supported)."
    )

# Define the image generation handler
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not MODEL_NAME:
        await update.message.reply_text("No suitable image generation model is available.")
        return

    prompt = update.message.text
    try:
        # Initialize the model dynamically
        imagen = genai.ImageGenerationModel(MODEL_NAME)

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
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN', '7711977179:AAFxPfbCD14LJLTekHKkHKTq6zRUCDscNEo')

    application = ApplicationBuilder().token(telegram_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
