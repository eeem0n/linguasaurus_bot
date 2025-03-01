from telegram.ext import CommandHandler, MessageHandler, filters
from file_manager import detect_file, upload, delete
from database import search_files, get_files_by_course, get_all_files_by_course

# start command
async def start(update, context):
    await update.message.reply_text("📚 Welcome to Linguasaurus, your go-to assistant for your journey in Linguistics! Use /help to see all available commands.")

# help command
async def help_command(update, context):
    pdf_path = "assets/coursecatalogue.pdf"
    help_text = (
        "here's the course catalogue\n"
        "use commands in this format:\n\n"
        "/books <course_code>\n"
        "/notes <course_code>\n"
        "/questions <course_code>\n"
        "/syllabus <course_code>\n\n"
        
        "/search <keyword>\n"
    )

    # send the help message immediately
    await update.message.reply_text(help_text, parse_mode="HTML")

    # check if the file exists before sending it
    if os.path.exists(pdf_path):
        try:
            with open(pdf_path, "rb") as pdf_file:
                await update.message.reply_document(
                    document=pdf_file, 
                    caption="📄 Course Catalogue"
                )
        except Exception as e:
            print(f"Error sending PDF: {e}") 
        
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
