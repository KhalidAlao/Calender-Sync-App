# 📅 Gmail to Google Calendar Sync

Automatically extract and schedule events from your Gmail into Google Calendar using Python, Google APIs, and natural language date parsing.

## 🚀 Overview

This project reads unread emails from a specific sender, intelligently parses event details (like date, time, and location), and creates calendar events—avoiding conflicts and duplicate scheduling.

🔧 Built with:
- Gmail API
- Google Calendar API
- Natural language date parsing (`dateparser`)
- Robust retry and logging system
- `.env` config support for deployment flexibility

---

## 🎯 Features

- 🔒 **OAuth2 Auth Flow** – Secure token-based access using `google-auth-oauthlib`
- 📬 **Email Filtering** – Targets only unread emails from configured senders
- 🧠 **Intelligent Parsing** – Extracts date, time, subject, and location using regex + NLP
- 📆 **Google Calendar Integration** – Adds events directly with conflict checking
- 🔁 **Retry Logic** – Retries failed operations (e.g., API downtime)
- 📄 **Logging** – Tracks sync process with timestamped logs
- 🌐 **Timezone Support** – Respects your local timezone via `.env` settings

---

## 📁 Project Structure

📦 gmail-calendar-sync/
┣ 📄 main.py # Entry point for syncing logic
┣ 📄 auth.py # Handles Google API authentication
┣ 📄 email_fetch.py # Gmail unread email fetching
┣ 📄 email_parser.py # Parses email text for event info
┣ 📄 calendar_utils.py # Calendar conflict check + event creation
┣ 📄 .env # Stores environment variables
┣ 📄 .gitignore # Hides credentials & logs
┗ 📄 sync.log # Runtime logs


🛠️ Installation

git clone https://github.com/KhalidAlao/Calender-Sync-App.git
cd gmail-calendar-sync

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt


🧪 Running the Script
Download your credentials.json from the Google Cloud Console (with Gmail & Calendar APIs enabled).
Place it in the project root.
Run the app:
python main.py
🔐 The first time, a browser will open to authenticate your Google account.
