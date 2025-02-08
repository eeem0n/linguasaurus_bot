from telegram import Update
from telegram.ext import CallbackContext
from database import save_file, delete_file_from_db  # ✅ Fixed Import
from config import ADMIN_IDS

# ✅ Temporary storage for uploaded files before saving them
pending_files = {}

# ✅ Detect when a file is uploaded
async def detect_file(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        return  # Ignore non-admins

    if update.message.document:
        file = update.message.document
        pending_files[user_id] = {"file_id": file.file_id, "file_name": file.file_name}
        await update.message.reply_text("📂 File received!\nNow enter: `/upload <category> <semester> <keywords>`")

# ✅ Upload the previously detected file with metadata
async def upload(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Only admins can upload files.")
        return

    # ✅ Check if a file was uploaded before this command
    if user_id not in pending_files:
        await update.message.reply_text("❌ No file detected.\nPlease send a file first, then use `/upload`.")
        return

    if len(context.args) < 3:
        await update.message.reply_text("❌ Usage: `/upload <category> <semester> <keywords>`\nExample: `/upload books 3 physics,science,formulas`")
        return

    category = context.args[0]
    semester = context.args[1]
    keywords = " ".join(context.args[2:])  # Store keywords

    file_data = pending_files.pop(user_id, None)  # ✅ Prevent KeyError
    if not file_data:
        await update.message.reply_text("❌ No pending file found. Please send the file again.")
        return

    file_id = file_data["file_id"]
    file_name = file_data["file_name"]

    save_file(file_id, file_name, category, semester, keywords)

    await update.message.reply_text(f"✅ File '{file_name}' saved under {category.capitalize()}, Semester {semester}.\n📌 Keywords: {keywords}")

# ✅ Delete file (Admins only)
async def delete(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Only admins can delete files.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: `/delete <file_name>`\nExample: `/delete physics_notes.pdf`")
        return

    file_name = " ".join(context.args)
    success = delete_file_from_db(file_name)  # ✅ Use correct function

    if success:
        await update.message.reply_text(f"✅ File '{file_name}' deleted.")
    else:
        await update.message.reply_text(f"❌ File '{file_name}' not found in the database.")

    file_name = " ".join(context.args)
    delete_file(file_name)
    await update.message.reply_text(f"✅ File '{file_name}' deleted.")
