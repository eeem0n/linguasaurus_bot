from telegram.ext import CommandHandler, MessageHandler, filters
from file_manager import detect_file, upload, delete
from database import search_files, get_files_by_course, get_all_files_by_course

# start command
async def start(update, context):
    await update.message.reply_text("📚 Welcome to Linguasaurus, your go-to assistant for your journey in Linguistics! Use /help to see all available commands.")

# help command
async def help_command(update, context):
    png_path = "assets/coursecatalogue-1.png" 
    help_text = (
        "/*here's the course catalougue* ⬆️\n"

        "/*retrieve files using these commands:*\n"
        "/books <course_code>\n"
        "/notes <course_code>\n"
        "/questions <course_code>\n"
        "/syllabus <course_code>\n"

        
        "/*search files*"
        "/search <keyword>\n"
    )
    with open(png_path, "rb") as png_file:
        await update.message.reply_document(document=png_file, caption=help_text, parse_mode='Markdown')


# retrieve files by category and course code
async def list_files(update, context):
    if len(context.args) < 1:
        category = update.message.text.split(" ")[0][1:]
        await update.message.reply_text("❌ usage: /{category} <course_code>\n" "✅ example: /books 1101 \n")
        return

    category = update.message.text.split(" ")[0][1:]  # extract category from command
    course_code = context.args[0]
    files = get_files_by_course(category, course_code)

    if not files:
        await update.message.reply_text(f"❌ no {category} found for course {course_code}.")
        return

    for file_name, file_id in files:
        await update.message.reply_document(file_id, caption=f"📄 {file_name}")



# search files by keyword
async def search(update, context):
    if len(context.args) < 1:
        await update.message.reply_text("❌ usage: /search <keyword>")
        return

    keyword = " ".join(context.args)
    results = search_files(keyword)

    if not results:
        await update.message.reply_text("❌ no matches found.")
        return

    for file_name, file_id in results:
        await update.message.reply_document(file_id, caption=f"📄 {file_name}")

# set up bot commands
def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("upload", upload))
    app.add_handler(CommandHandler("books", list_files))
    app.add_handler(CommandHandler("notes", list_files))
    app.add_handler(CommandHandler("questions", list_files))
    app.add_handler(CommandHandler("syllabus", list_files))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(MessageHandler(filters.Document.ALL, detect_file))
