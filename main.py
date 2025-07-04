import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from fpdf import FPDF

BOT_TOKEN = os.getenv("BOT_TOKEN")
AD_TEXT = "🌟 @Tilmochgpt_bot ni sinab ko‘ring — AI yordamida tez va mukammal tarjima qiladi!"
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

user_images = {}
user_tasks = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📌 Rasm(lar)ni yuboring. Bot biroz kutib rasm to‘plamini qabul qiladi va PDF yaratishga tayyor bo‘ladi.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    photos = update.message.photo
    if not photos:
        return

    photo = photos[-1]
    file = await context.bot.get_file(photo.file_id)

    file_path = f"{TEMP_DIR}/{user_id}_{len(user_images.get(user_id, [])) + 1}.jpg"
    await file.download_to_drive(file_path)

    user_images.setdefault(user_id, []).append(file_path)

    # Agar oldingi task bo'lsa, bekor qilamiz
    if user_id in user_tasks:
        user_tasks[user_id].cancel()

    # Yangi task ishga tushiramiz
    task = asyncio.create_task(schedule_summary(update, context, user_id))
    user_tasks[user_id] = task

async def schedule_summary(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    try:
        await asyncio.sleep(5)
        count = len(user_images.get(user_id, []))
        text = (
            f"✅ {count} ta rasm qabul qilindi.\n"
            f"{AD_TEXT}"
        )
        keyboard = [[InlineKeyboardButton("📄 PDF yaratishni boshlash", callback_data="create_pdf")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
    except asyncio.CancelledError:
        pass  # Agar task bekor qilinsa, hech narsa qilmaymiz

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "create_pdf":
        if user_id not in user_images or not user_images[user_id]:
            await query.edit_message_text("⚠ Rasm yubormagansiz.")
            return

        await query.edit_message_text("✅ PDF tayyorlanmoqda. Iltimos, biroz  kuting.\n" + AD_TEXT)

        pdf_path = f"{TEMP_DIR}/{user_id}_output.pdf"
        pdf = FPDF()
        for img_path in user_images[user_id]:
            pdf.add_page()
            pdf.image(img_path, x=10, y=10, w=190)
        pdf.output(pdf_path)

        await asyncio.sleep(30)

        await context.bot.send_document(chat_id=user_id, document=open(pdf_path, 'rb'))

        for img_path in user_images[user_id]:
            os.remove(img_path)
        os.remove(pdf_path)
        user_images[user_id] = []

        await context.bot.send_message(chat_id=user_id, text="✅ PDF yuborildi va vaqtinchalik fayllar o‘chirildi.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
