from telegram import Update
from telegram.ext import CallbackContext
from database import save_file, delete_file
from config import ADMIN_IDS

# allowed categories
ALLOWED_CATEGORIES = ["books", "notes", "questions", "syllabus", "routine"]

# temporary storage for uploaded files
pending_files = {}

# detect file upload
async def detect_file(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        return  # ignore non-admins

    if update.message.document:
        file = update.message.document
        pending_files[user_id] = {"file_id": file.file_id, "file_name": file.file_name}
        await update.message.reply_text(
            "📂 file received! now enter: /upload <category> <course_code> <keywords>\n"
        )

# upload file to database
async def upload(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ only admins can upload files.")
        return

    if user_id not in pending_files:
        await update.message.reply_text("❌ no file detected. please send a file first, then use /upload.")
        return

    if len(context.args) < 3:
        await update.message.reply_text(
            "❌ usage: /upload <category> <course_code> <keywords>\n"
        )
        return

    category = context.args[0].lower()  # convert to lowercase
    course_code = context.args[1]
    keywords = " ".join(context.args[2:])

    # validate category
    if category not in ALLOWED_CATEGORIES:
        await update.message.reply_text(
            "❌ invalid category! choose from:\n"
            "books, notes, questions, syllabus, routine"
        )
        return

    file_data = pending_files.pop(user_id, None)
    if not file_data:
        await update.message.reply_text("❌ no pending file found. please send the file again.")
        return

    file_id = file_data["file_id"]
    file_name = file_data["file_name"]

    # save to database
    success = save_file(file_id, file_name, category, course_code, keywords)

    if success:
        await update.message.reply_text(
            f"✅ file '{file_name}' saved under **{category.capitalize()}** for course **{course_code}**.\n"
            f"📌 keywords: {keywords}"
        )
    else:
        await update.message.reply_text(f"⚠️ file '{file_name}' already exists in the database.")

# delete a file (admin-only)
async def delete(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ only admins can delete files.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("❌ usage: /delete <file_name>")
        return

    file_name = " ".join(context.args)
    delete_file(file_name)
    await update.message.reply_text(f"✅ file '{file_name}' deleted.")


