# Linguasaurus Bot

Linguasaurus Bot is a Telegram bot designed to assist students in the Department of Linguistics of a University. It provides an easy way to store, retrieve, and manage resources, including PDFs, slides and other data through simple commands.

---

## Features

- Store and retrieve **Linguistics resources** based on course code.
- Upload and access **documents**
- Search and retrieve by **keywords** from stored metadata.
- Built using **Python, Telegram API and PostgreSQL** for efficient data management.

---

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/eeem0n/linguasaurus_bot.git
cd linguasaurus_bot
```

### 2. Install Dependencies
Ensure Python 3.9+ is installed, then run:
```sh
pip install -r requirements.txt
```

### 3. Configure the Bot
Create a `.env` file in the root directory and add your Telegram Bot Token and Database URL:
```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
ADMIN_IDS=telegram_admin_ids
DATABASE_URL=your-database-url
```

### 4. Run the Bot
```sh
python bot.py
```
The bot should now be running and ready to use.

---

## License

This project is licensed under the **MIT License**. See **LICENSE** for more details.
