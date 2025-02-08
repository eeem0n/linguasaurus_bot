from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from handlers import setup_handlers
from logger import log_error  # Import logger

app = ApplicationBuilder().token(BOT_TOKEN).build()
setup_handlers(app)

# Handle errors globally
app.add_error_handler(log_error)

print("🤖 Linguasaurus is running...")
app.run_polling()
