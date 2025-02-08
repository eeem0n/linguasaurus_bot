from telegram import Update
from telegram.ext import CallbackContext
from database import save_file, delete_file
from config import ADMIN_IDS

# Upload a file by replying to it
async def upload(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Only admins can upload files.")
        return

    # Detect file from a reply (if not in the same message)
    file = update.message.document or (update.message.reply_to_message and update.message.reply_to_message.document)

    if not file:
        await update.message.reply_text("❌ Please send a file first, then reply to it with `/upload <category> <semester> <keywords>`")
        return

    if len(context.args) < 3:
        await update.message.reply_text("❌ Usage: `/upload <category> <semester> <keywords>`\nExample: `/upload books 3 physics,science,formulas`")
        return

    category = context.args[0]
    semester = context.args[1]
    keywords = " ".join(context.args[2:])  # Store keywords

    file_id = file.file_id
    file_name = file.file_name

    save_file(file_id, file_name, category, semester, keywords)
    await update.message.reply_text(f"✅ File '{file_name}' saved under {category.capitalize()}, Semester {semester}.\n📌 Keywords: {keywords}")

#  Download file by name
async def download(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: `/download <file_name>`\nExample: `/download physics_notes.pdf`")
        return

    file_name = " ".join(context.args)
    file_id = get_file_id_by_name(file_name)

    if file_id:
        await update.message.reply_document(file_id, filename=file_name)
    else:
        await update.message.reply_text("❌ File not found.")
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
