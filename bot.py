import os
import random
from telegram import Update
import time
from telegram.ext import Application, CommandHandler, ContextTypes
import os
token = os.getenv("TOKEN")


# Your bot token
BOT_TOKEN = "7673483122:AAGyk8HAfVJ6D0_xzgJZTtgnhyqpnwXx-2c"

# Folder containing your images
IMAGE_FOLDER = "images"

# Start time of the bot
START_TIME = time.time()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the user starts the bot."""
    await update.message.reply_text("Hi! Send /image to get a random image.")

async def send_random_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random image from the image folder."""
    try:
        # Get all image files in the folder
        image_files = [f for f in os.listdir("public") if f.endswith((".png", ".jpg", ".jpeg", ".jfif"))]
        
        if not image_files:
            await update.message.reply_text("No images available!")
            return

        # Pick a random image
        random_image = random.choice(image_files)
        image_path = os.path.join("public", random_image)

        # Send the image
        with open(image_path, "rb") as image:
            await update.message.reply_photo(image)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a list of available commands."""
    help_text = """
    Here are the available commands:
    /start - Start the bot or wake it up
    /help - Display this help message
    /image - Get a random image from the bot
    """
    await update.message.reply_text(help_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check the bot's uptime and functionality."""
    current_time = time.time()
    uptime_seconds = int(current_time - START_TIME)

    # Convert uptime into hours, minutes, and seconds
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    status_text = f"""
    Bot Status:
    ✅ Online and Functional
    ⏱️ Uptime: {hours} hours, {minutes} minutes, {seconds} seconds
    """
    await update.message.reply_text(status_text)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if the bot is responsive."""
    await update.message.reply_text("Pong!")
    
def main():
    """Main function to start the bot."""
    # Create the bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("image", send_random_image))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("ping", ping))  # Added /ping command


    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
