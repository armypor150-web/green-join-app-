import os
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBAPP_URL = os.environ["WEBAPP_URL"]  # Your HTTPS app URL, e.g. https://example.com
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("OPEN JOIN APP", web_app=WebAppInfo(url=WEBAPP_URL)))
    bot.send_message(
        message.chat.id,
        "Welcome! Open the app below, join all required channels, then tap Check Joined.",
        reply_markup=kb
    )

def run_bot():
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    from app import app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
