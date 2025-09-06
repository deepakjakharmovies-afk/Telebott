

import nest_asyncio
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

nest_asyncio.apply()
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Error: BOT_TOKEN environment variable not set")


# Placeholder links
DIRECT_LINK = "You have to buy premium first\ntry shortened link"
SHORTENED_LINK = "https://shrinkme.top/prmbkM2" # Replace with your actual shortened link logic

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"/start received from {user.first_name} ({user.id})")

    # Add a "Start" button to the initial message
    keyboard = [
        [InlineKeyboardButton("Start", callback_data="show_language_options")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\nTap the button to start:",
        reply_markup=reply_markup
    )

# Handler for initial start button and subsequent actions
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if query.data == "show_language_options":
        logger.info(f"Start button clicked by {user.first_name}")
        keyboard = [
            [InlineKeyboardButton("English", callback_data="lang_en")],
            [InlineKeyboardButton("Hindi", callback_data="lang_hi")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"👋 Welcome {user.first_name}!\nPlease select your language:",
            reply_markup=reply_markup
        )

    elif query.data == "lang_en":
        logger.info(f"English button clicked by {user.first_name}")
        keyboard = [
            [InlineKeyboardButton("Send Direct Link", callback_data="link_direct_en")],
            [InlineKeyboardButton("Send Shortened Link", callback_data="link_shortened_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "✅ Language set to English.\n\nHello! 👋 How are you?\nPlease select a link option:",
            reply_markup=reply_markup
        )
    elif query.data == "lang_hi":
        logger.info(f"Hindi button clicked by {user.first_name}")
        keyboard = [
            [InlineKeyboardButton("सीधा लिंक भेजें", callback_data="link_direct_hi")],
            [InlineKeyboardButton("छोटा लिंक भेजें", callback_data="link_shortened_hi")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "✅ भाषा हिंदी चुनी गई।\n\nनमस्ते! 🙏 आप कैसे हैं?\nकृपया एक लिंक विकल्प चुनें:",
            reply_markup=reply_markup
        )
    elif query.data == "link_direct_en":
        logger.info(f"Direct link (English) requested by {user.first_name}")
        await query.edit_message_text(f"Here is the direct link: {DIRECT_LINK}")
    elif query.data == "link_shortened_en":
        logger.info(f"Shortened link (English) requested by {user.first_name}")
        await query.edit_message_text(f"Here is the shortened link: {SHORTENED_LINK}")
    elif query.data == "link_direct_hi":
        logger.info(f"Direct link (Hindi) requested by {user.first_name}")
        await query.edit_message_text(f"यहां सीधा लिंक है: {DIRECT_LINK}")
    elif query.data == "link_shortened_hi":
        logger.info(f"Shortened link (Hindi) requested by {user.first_name}")
        await query.edit_message_text(f"यहां छोटा लिंक है: {SHORTENED_LINK}")


# Main
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback)) # Handle all callbacks

    print("🤖 Bot is running... now try /start in Telegram or tap the Start button.")
    await app.run_polling()

await main()
