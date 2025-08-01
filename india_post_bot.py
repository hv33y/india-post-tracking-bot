import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Please set the TELEGRAM_BOT_TOKEN environment variable")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 Welcome to the India Post Tracking Bot!\n\n"
        "Use /track <tracking_number> to check your parcel status.\n\n"
        "Example:\n/track EK123456789IN"
    )

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗ Usage: /track <tracking_number>\nExample: /track EH145148738IN")
        return

    tracking_number = context.args[0].strip().upper()

    if not tracking_number.endswith("IN") or len(tracking_number) != 13:
        await update.message.reply_text("⚠️ That doesn't look like a valid India Post tracking number.")
        return

    await update.message.reply_text("🔍 Fetching tracking info...")
    status = get_india_post_status(tracking_number)
    await update.message.reply_text(status)

def get_india_post_status(tracking_number: str) -> str:
    url = "https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/TrackConsignment.aspx"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    session = requests.Session()
    try:
        response = session.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")

        viewstate = soup.find("input", {"id": "__VIEWSTATE"})["value"]
        eventvalidation = soup.find("input", {"id": "__EVENTVALIDATION"})["value"]

        payload = {
            "__VIEWSTATE": viewstate,
            "__EVENTVALIDATION": eventvalidation,
            "ctl00$ContentPlaceHolder1$txtConsignment": tracking_number,
            "ctl00$ContentPlaceHolder1$btnSearch": "Search"
        }

        post_response = session.post(url, data=payload, headers=headers, timeout=15)
        soup = BeautifulSoup(post_response.content, "html.parser")
        table = soup.find("table", {"class": "table_border"})

        if not table:
            return f"❌ No tracking info found for `{tracking_number}`.\nPlease check the number and try again."

        rows = table.find_all("tr")[1:]  # Skip header row
        if not rows:
            return f"⚠️ No updates available for `{tracking_number}` yet."

        message = f"📬 **Tracking updates for `{tracking_number}`:**\n\n"
        for row in rows[:3]:  # Show latest 3 updates
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) >= 4:
                message += f"📅 *{cols[0]}*\n📍 {cols[1]}\n📦 {cols[2]}\n📝 {cols[3]}\n\n"

        return message.strip()

    except Exception as e:
        logging.error(f"Error fetching status: {e}")
        return "❌ An error occurred while fetching tracking information. Try again later."

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("track", track))
    app.run_polling()
