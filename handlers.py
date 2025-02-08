from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from keyboards import semester_menu, back_button  
from database import get_files_by_category, search_files
from file_manager import upload, delete


# Start Command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("📚 Welcome to Linguasaurus, your go-to assistant for your journey with Linguistics! Use /help to see commands.")

# Help Command
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "You can control me by sending these commands:\n"
        "\n"
        "/books - browse books \n"
        "/notes - browse notes \n"
        "/questions - browse past questions \n"
        "/syllabus - view syllabus \n"
        "/routine - view schedule \n"
        "/search <keyword> - search materials \n"
    )

# Show semester selection
async def show_semester_menu(update: Update, context: CallbackContext):
    category = update.message.text.replace("/", "")  # Extract category from command
    await update.message.reply_text(f"📂 Select a semester for {category.capitalize()}:", reply_markup=semester_menu(category))

# Handle semester selection
async def handle_semester_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    category, semester = query.data.split("_semester_")
    files = get_files_by_category(f"{category}_semester_{semester}")
    
    message = "📂 " + category.capitalize() + " for Semester " + semester + ":\n"
    message += "\n".join(files) if files else "❌ No files found."
    
    # Show files with a "Back" button
    await query.edit_message_text(message, reply_markup=back_button())

# Search function
async def search(update: Update, context: CallbackContext):
    query = " ".join(context.args)
    results = search_files(query)
    await update.message.reply_text("🔍 Search Results:\n" + "\n".join(results) if results else "❌ No matches found.")


# Handle back button (returns to semester selection)
async def handle_back(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    category = query.message.text.split(" ")[1].lower()  # Extract category from message
    await query.edit_message_text(f"📂 Select a semester for {category.capitalize()}:", reply_markup=semester_menu(category))

#  Set Up Handlers
def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("books", show_semester_menu))
    app.add_handler(CommandHandler("notes", show_semester_menu))
    app.add_handler(CommandHandler("questions", show_semester_menu))
    app.add_handler(CommandHandler("syllabus", show_semester_menu))
    app.add_handler(CommandHandler("routine", show_semester_menu))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("upload", upload))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CallbackQueryHandler(handle_semester_selection, pattern=".*_semester_"))
    app.add_handler(CallbackQueryHandler(handle_back, pattern="go_back"))  # Handle back button
