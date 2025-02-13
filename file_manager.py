from telegram import Update
from telegram.ext import CallbackContext
from database import save_file, delete_file
from config import ADMIN_IDS

# ✅ Allowed categories
ALLOWED_CATEGORIES = ["books", "notes", "questions", "syllabus", "routine"]

# ✅ Temporary storage for uploaded files
pending_files = {}

# ✅ Detect file upload
async def detect_file(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        return  # Ignore non-admins

    if update.message.document:
        file = update.message.document
        pending_files[user_id] = {"file_id": file.file_id, "file_name": file.file_name}
        await update.message.reply_text(
            "📂 File received! Now enter: `/upload <category> <course_code> <keywords>`\n"
            "Example: `/upload books 1101 linguistics, syntax`"
        )

# ✅ Upload file to database
async def upload(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Only admins can upload files.")
        return

    if user_id not in pending_files:
        await update.message.reply_text("❌ No file detected. Please send a file first, then use `/upload`.")
        return

    if len(context.args) < 3:
        await update.message.reply_text(
            "❌ Usage: `/upload <category> <course_code> <keywords>`\n"
            "Example: `/upload books 1101 linguistics, syntax`"
        )
        return

    category = context.args[0].lower()  # Convert to lowercase
    course_code = context.args[1]
    keywords = " ".join(context.args[2:])

    # ✅ Validate category
    if category not in ALLOWED_CATEGORIES:
        await update.message.reply_text(
            "❌ Invalid category! Choose from:\n"
            "`books`, `notes`, `questions`, `syllabus`, `routine`"
        )
        return

    file_data = pending_files.pop(user_id, None)
    if not file_data:
        await update.message.reply_text("❌ No pending file found. Please send the file again.")
        return

    file_id = file_data["file_id"]
    file_name = file_data["file_name"]

    # ✅ Save to database
    success = save_file(file_id, file_name, category, course_code, keywords)

    if success:
        await update.message.reply_text(
            f"✅ File '{file_name}' saved under **{category.capitalize()}** for course **{course_code}**.\n"
            f"📌 Keywords: `{keywords}`"
        )
    else:
        await update.message.reply_text(f"⚠️ File '{file_name}' already exists in the database.")

# ✅ Delete a file (Admin-only)
async def delete(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Only admins can delete files.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: `/delete <file_name>`")
        return

    file_name = " ".join(context.args)
    delete_file(file_name)
    await update.message.reply_text(f"✅ File '{file_name}' deleted.")


