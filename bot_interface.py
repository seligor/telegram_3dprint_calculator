import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import threading
from handlers import handle_stl_file
from callbacks import button_callback
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ENGINEER_USER_ID = os.getenv("ENGINEER_USER_ID")

if TELEGRAM_BOT_TOKEN is None:
    logger.error("TELEGRAM_BOT_TOKEN не задан в .env файле.")
if ENGINEER_USER_ID is None:
    logger.error("ENGINEER_USER_ID не задан в .env файле.")
else:
    try:
        ENGINEER_USER_ID = int(ENGINEER_USER_ID)
    except ValueError:
        logger.error("ENGINEER_USER_ID не является допустимым числом.")
        ENGINEER_USER_ID = None


MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
TEMP_DIR = os.getenv("TEMP_DIR")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Отправь мне STL файл.')


async def process_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    document = message.document

    logger.info(f"Загружен файл: {document.file_name}, Размер: {document.file_size} байт, MIME-тип: {document.mime_type}")

    if document.file_size > MAX_FILE_SIZE_BYTES:
        await message.reply_text(f"Файл слишком большой. Максимальный размер: {MAX_FILE_SIZE_MB} МБ.")
        return

    if document.file_name.lower().endswith('.stl') and (document.mime_type in {"model/stl", "application/vnd.ms-pki.stl"}):
        await handle_stl_file(update, context)
    else:
        await message.reply_text("Файл не является STL или имеет неподходящий MIME-тип.")


def remove_old_files():
    """Удаляет файлы старше одного часа из каталога TEMP_DIR."""
    while True:
        current_time = time.time()
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)

            if os.path.isfile(file_path):
                file_mod_time = os.path.getmtime(file_path)
                if current_time - file_mod_time > 3600:  # 3600 секунд в часе
                    try:
                        os.remove(file_path)
                        logger.info(f"Удалён старый файл: {file_path}")
                    except Exception as e:
                        logger.error(f"Ошибка при удалении файла {file_path}: {e}")

        time.sleep(60)  # Пауза 60 секунд перед следующей проверкой


def main():
    threading.Thread(target=remove_old_files, daemon=True).start()
    token = TELEGRAM_BOT_TOKEN
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, process_document))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()


if __name__ == '__main__':
    main()
