from telegram.ext import CommandHandler, MessageHandler, filters
from file_manager import detect_file, upload, delete
from database import search_files, get_files_by_course, get_all_files_by_course

# ✅ Start Command
async def start(update, context):
    await update.message.reply_text("📚 Welcome to Linguasaurus! Use /help to see available commands.")

# ✅ Help Command
async def help_command(update, context):
    await update.message.reply_text(
        "/books <course_code>\n"
        "/notes <course_code>\n"
        "/questions <course_code>\n"
        "/syllabus <course_code>\n"
        "/routine <course_code>\n"
        "/files <course_code>\n"
        "/search <keyword>\n"
    )

# ✅ Retrieve files by category and course code
async def list_files(update, context):
    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: `/books <course_code>`")
        return

    category = update.message.text.split(" ")[0][1:]  # Extract category from command
    course_code = context.args[0]
    files = get_files_by_course(category, course_code)

    if not files:
        await update.message.reply_text(f"❌ No {category} found for course {course_code}.")
        return

    for file_name, file_id in files:
        await update.message.reply_document(file_id, caption=f"📄 {file_name}")

# ✅ List all files for a course
async def list_all_files(update, context):
    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: `/files <course_code>`")
        return

    course_code = context.args[0]
    files_by_category = get_all_files_by_course(course_code)

    if not files_by_category:
        await update.message.reply_text(f"❌ No files found for course {course_code}.")
        return

    # Send files category by category
    for category, files in files_by_category.items():
        message = f"📂 **{category.capitalize()} for {course_code}**:\n"
        for file_name, _ in files:
            message += f"📄 {file_name}\n"

        await update.message.reply_text(message, parse_mode="Markdown")

        # Send files one by one
        for file_name, file_id in files:
            await update.message.reply_document(file_id, caption=f"📄 {file_name}")

# ✅ Search files by keyword
async def search(update, context):
    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: `/search <keyword>`")
        return

    keyword = " ".join(context.args)
    results = search_files(keyword)

    if not results:
        await update.message.reply_text("❌ No matches found.")
        return

    for file_name, file_id in results:
        await update.message.reply_document(file_id, caption=f"📄 {file_name}")

# ✅ Set up bot commands
def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("upload", upload))
    app.add_handler(CommandHandler("books", list_files))
    app.add_handler(CommandHandler("notes", list_files))
    app.add_handler(CommandHandler("questions", list_files))
    app.add_handler(CommandHandler("syllabus", list_files))
    app.add_handler(CommandHandler("routine", list_files))
    app.add_handler(CommandHandler("files", list_all_files))  # NEW COMMAND
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(MessageHandler(filters.Document.ALL, detect_file))
