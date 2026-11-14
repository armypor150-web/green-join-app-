import os, json, hmac, hashlib, time
from dotenv import load_dotenv
load_dotenv()

from urllib.parse import parse_qsl
from flask import Flask, request, jsonify, send_from_directory
import telebot

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__, static_folder="static")

# Configure all seven channels here.
# chat_id is used for membership checks; join_url is shown in the app.
CHANNELS = [
    {"title": "Channel 1", "chat_id": "@freepennal123", "join_url": "https://t.me/freepennal123"},
    {"title": "Channel 2", "chat_id": "@freefireidsolutionindia", "join_url": "https://t.me/freefireidsolutionindia"},
    {"title": "Channel 3", "chat_id": "@permosan", "join_url": "https://t.me/permosan"},
    {"title": "Channel 4", "chat_id": "@SONUGAMERXFREEPANEL", "join_url": "https://t.me/SONUGAMERXFREEPANEL"},
    {"title": "Channel 5", "chat_id": "", "join_url": "https://t.me/+o4iqjslSf1g1NWI9"},
    {"title": "Channel 6", "chat_id": "", "join_url": "https://t.me/your_channel_6"},
    {"title": "Channel 7", "chat_id": "@panelpaidfree", "join_url": "https://t.me/panelpaidfree"},
]

def verify_init_data(init_data: str):
    """Validate Telegram Mini App initData and return its user object."""
    if not init_data:
        raise ValueError("Missing Telegram initData")
    values = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = values.pop("hash", None)
    if not received_hash:
        raise ValueError("Missing initData hash")
    # Telegram Web Apps validation algorithm
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(values.items()))
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calculated, received_hash):
        raise ValueError("Invalid Telegram initData signature")
    auth_date = int(values.get("auth_date", "0"))
    if abs(int(time.time()) - auth_date) > 86400:
        raise ValueError("Expired Telegram initData")
    user = json.loads(values.get("user", "{}"))
    if not user.get("id"):
        raise ValueError("Telegram user not found")
    return user

@app.get("/")
def index():
    return send_from_directory("static", "index.html")

@app.get("/api/channels")
def channels():
    return jsonify([{"title": c["title"], "join_url": c["join_url"]} for c in CHANNELS])

@app.post("/api/check")
def check():
    try:
        payload = request.get_json(force=True)
        user = verify_init_data(payload.get("initData", ""))
        user_id = int(user["id"])
        missing = []
        for channel in CHANNELS:
            chat_id = channel["chat_id"].strip()
            if not chat_id:
                missing.append(channel["title"] + " (configure chat_id)")
                continue
            try:
                member = bot.get_chat_member(chat_id, user_id)
                if member.status not in ("member", "administrator", "creator") and not (
                    member.status == "restricted" and getattr(member, "is_member", False)
                ):
                    missing.append(channel["title"])
            except Exception:
                # Most often: wrong chat_id or bot is not an admin/member of that channel.
                missing.append(channel["title"] + " (check bot admin / chat_id)")
        return jsonify({"ok": len(missing) == 0, "missing": missing})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
