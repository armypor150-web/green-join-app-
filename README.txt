GREEN JOIN TELEGRAM MINI APP (Python)

1) Install Python 3.10+.
2) Run: pip install -r requirements.txt
3) Copy .env.example to .env, then set BOT_TOKEN and WEBAPP_URL.
   Set environment variables in your hosting dashboard (recommended).
4) Deploy this project on a public HTTPS host.
5) In BotFather, set the Mini App domain for your bot (/setdomain) to your domain.
6) Set WEBAPP_URL to the deployed HTTPS URL.
7) Start: python bot.py
8) Open your bot and send /start. Tap OPEN JOIN APP.

IMPORTANT CHANNEL SETUP:
- Replace every CHANNELS entry in app.py with the correct chat_id and join_url.
- For public channels, chat_id can be @channelusername.
- For private channels, use the numeric -100... chat ID, not the invite link.
- Add the bot as an administrator to every channel so getChatMember can verify users.
- Channel 5 and Channel 6 are intentionally left blank until you provide their real numeric chat IDs / usernames.
- Do not publish your bot token or put it in index.html.
- Telegram Mini Apps require HTTPS and must be opened from Telegram.
