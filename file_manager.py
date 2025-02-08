from telegram import Update
from telegram.ext import CallbackContext
from database import save_file, delete_file
from config import ADMIN_IDS

# Upload file (Admins only)
async def upload(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Only admins can upload files.")
        return

    if not update.message.document:
        await update.message.reply_text("❌ Please upload a file.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: `/upload <category> <semester>`")
        return

    category = context.args[0]
    semester = context.args[1]

    file = update.message.document
    save_file(file.file_id, file.file_name, category, semester)
    await update.message.reply_text(f"✅ File '{file.file_name}' saved under {category.capitalize()}, Semester {semester}.")

# Delete file (Admins only)
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
