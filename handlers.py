from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler
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

    try:
        with open(pdf_path, "rb") as pdf_file:
            await update.message.reply_document(caption=help_text, document=pdf_file)
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
        
# retrieve files by category and course code
async def list_files(update, context):
    if len(context.args) < 1:
        category = update.message.text.split(" ")[0][1:]
        await update.message.reply_text(f"❌ usage: /{category} <course_code>\n✅ example: /books 1101\n")
        return

    category = update.message.text.split(" ")[0][1:]  # extract category from command
    course_code = context.args[0]
    files = get_files_by_course(category, course_code)

    if not files:
        await update.message.reply_text(f"❌ no {category} found for course {course_code}.")
        return

    buttons = []
    for file_name, file_id in files:
        buttons.append([InlineKeyboardButton(file_name, callback_data=f"{category}:{file_id}")])
    
    # Add a "Get All" button
    buttons.append([InlineKeyboardButton("Get All", callback_data=f"{category}:all:{course_code}")])
    
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(f"Select a file to download for course {course_code}:", reply_markup=reply_markup)

# handle file selection
async def file_selection(update, context):
    query = update.callback_query
    await query.answer()
    
    data = query.data.split(":")
    category = data[0]
    file_id = data[1]
    
    if file_id == "all":
        course_code = data[2]
        files = get_files_by_course(category, course_code)
        for file_name, file_id in files:
            await query.message.reply_document(file_id, caption=f"📄 {file_name}")
    else:
        # Get the file name from the file_id if needed
        file_name = "Selected File"  # Replace with the actual file name if needed
        await query.message.reply_document(file_id, caption=f"📄 {file_name}")

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

    buttons = []
    for file_name, file_id in results:
        buttons.append([InlineKeyboardButton(file_name, callback_data=f"search:{file_id}")])
    
    # Add a "Get All" button
    buttons.append([InlineKeyboardButton("Get All", callback_data=f"search:all:{keyword}")])
    
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Select a file to download:", reply_markup=reply_markup)

# handle search selection
async def search_selection(update, context):
    query = update.callback_query
    await query.answer()
    
    data = query.data.split(":")
    action = data[0]
    file_id = data[1]
    
    if file_id == "all":
        keyword = data[2]
        results = search_files(keyword)
        for file_name, file_id in results:
            await query.message.reply_document(file_id, caption=f"📄 {file_name}")
    else:
        # Get the file name from the file_id if needed
        file_name = "Selected File"  # Replace with the actual file name if needed
        await query.message.reply_document(file_id, caption=f"📄 {file_name}")

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
    app.add_handler(CallbackQueryHandler(file_selection, pattern="^(books|notes|questions|syllabus):"))
    app.add_handler(CallbackQueryHandler(search_selection, pattern="^search:"))
    app.add_handler(MessageHandler(filters.Document.ALL, detect_file))
