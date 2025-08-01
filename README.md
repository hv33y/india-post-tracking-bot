# India Post Speed Post (Telegram Tracking Bot)

This Telegram bot lets you track India Post Speed Post shipments by entering a single tracking number.

## Features

- Track single India Post Speed Post tracking number at a time
- Fetches live status updates from the official India Post website
- Displays the latest 3 tracking updates
- Simple `/track <tracking_number>` command interface

## Setup & Usage

### 1. Clone the repository
```bash
git clone https://github.com/hv33y/india-post-tracking-bot.git
cd india-post-tracking-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Telegram bot token as an environment variable
Replace **YOUR_TELEGRAM_BOT_TOKEN** with your actual bot token from [@BotFather](https://t.me/BotFather).

On Linux/macOS:
```bash
export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
```

On Windows (PowerShell):
```bash
setx TELEGRAM_BOT_TOKEN "YOUR_TELEGRAM_BOT_TOKEN"
```

### 4. Run the bot
```bash
python india_post_bot.py
```

### 5. Use the bot on Telegram
- Send ```/start``` to get welcome message
- Send ```/track <tracking_number>``` to get the latest tracking status

Example:
```/track EK123456789IN```

## Notes
- The bot scrapes the India Post tracking website, so if the site changes, the bot might need updating.
- Only single tracking number queries are supported.
- For continuous running on VPS, consider using screen, tmux, or systemd service.
