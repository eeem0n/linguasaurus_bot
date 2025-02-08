import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename="bot.log",  # Logs are saved in bot.log
    filemode="a"  # Append logs instead of overwriting
)

def log_error(update, context):
    """Log errors caused by updates."""
    logging.error(f"Update {update} caused error {context.error}")
