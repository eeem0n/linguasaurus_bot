from telegram.ext import CommandHandler, MessageHandler, filters
from file_manager import detect_file, upload, delete
from database import search_files, get_files_by_course

#  Start Command
async def start(update, context):
    await update.message.reply_text("📚 Welcome to Linguasaurus! Use /help to see all available commands.")

#  Help Command
async def help_command(update, context):
    await update.message.reply_text(
        "/books <course_code> - view books for a course\n"
        "/notes <course_code> - view notes for a course\n"
        "/questions <course_code> - view past questions\n"
        "/syllabus <course_code> - view syllabus\n"
        "/routine <course_code> - view routine\n"
        "/search <keyword> - search materials\n"
    )

#  Retrieve files by category and course code
async def list_files(update, context):
    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: /books <course_code>")
        return

    category = update.message.text.split(" ")[0][1:]  # Extract category from command
    course_code = context.args[0]
    files = get_files_by_course(category, course_code)

    if not files:
        await update.message.reply_text("❌ No files found.")
        return

    for file_name, file_id in files:
        await update.message.reply_document(file_id, caption=f"📄 {file_name}")

#  Search files by keyword
async def search(update, context):
    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: /search <keyword>")
        return

    keyword = " ".join(context.args)
    results = search_files(keyword)

    if not results:
        await update.message.reply_text("❌ No matches found.")
        return

    for file_name, file_id in results:
        await update.message.reply_document(file_id, caption=f"📄 {file_name}")

#  Set up bot commands
def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("upload", upload))
    app.add_handler(CommandHandler("books", list_files))
    app.add_handler(CommandHandler("notes", list_files))
    app.add_handler(CommandHandler("questions", list_files))
    app.add_handler(CommandHandler("syllabus", list_files))
    app.add_handler(CommandHandler("routine", list_files))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(MessageHandler(filters.Document.ALL, detect_file))
