from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
import os

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    user_link = f"[{user.first_name}](tg://user?id={user.id})"

    if query.data == 'confirm_yes':
        try:
            file_path = context.user_data['file_path']
            image_path = context.user_data['image_path']

            caption_text = (
                f"Файл от {user_link}.\n"
                f"Объём модели: {context.user_data['volume']:.2f} мм³\n"
                f"Количество пластика: {context.user_data['mass']:.2f} г\n"
                f"Примерное время печати: {context.user_data['print_time']:.2f} минут\n"
                f"Стоимость печати: {context.user_data['cost']:.2f} рублей"
            )

            await context.bot.send_document(
                chat_id=os.getenv("ENGINEER_USER_ID"),
                document=open(file_path, 'rb'),
                caption=caption_text,
                parse_mode='Markdown'
            )
            await context.bot.send_photo(
                chat_id=os.getenv("ENGINEER_USER_ID"),
                photo=open(image_path, 'rb')
            )
            await query.edit_message_text("Информация передана, ожидайте ответа инженера.")
        except Exception as e:
            logger.error(f"Ошибка при отправке: {str(e)}")
            await query.edit_message_text(f"Ошибка при отправке: {str(e)}")

    elif query.data == 'confirm_no':
        await query.edit_message_text("Отправка отменена. Отправьте новый файл.")

    os.remove(context.user_data['file_path'])
    os.remove(context.user_data['image_path'])
    context.user_data.clear()
