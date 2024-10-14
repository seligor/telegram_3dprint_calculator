from loguru import logger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import time
import os
from stl_processing import load_stl, visualize_stl
from print_calculations import calculate_print_time
from gcode_processing import process_gcode  # Импортируем функцию для обработки G-code

from dotenv import load_dotenv
load_dotenv()

TEMP_DIR = os.getenv("TEMP_DIR")

async def handle_stl_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message
        document = message.document

        # Определение пользователя
        user_id = message.from_user.id
        user_name = message.from_user.first_name

        timestamp = int(time.time())
        file_path = f'{TEMP_DIR}/temp_{user_id}_{timestamp}.stl'
        image_path = f'{TEMP_DIR}/stlvisualization_{user_id}_{timestamp}.png'

        await message.reply_text("Файл принят. Начинаю обработку...")

        file = await document.get_file()
        await file.download_to_drive(file_path)

        stl_mesh = load_stl(file_path)
        visualize_stl(stl_mesh, image_path)

        # Получаем путь к файлу G-code
        gcode_file_path = calculate_print_time(file_path)

        # Обрабатываем G-code и получаем параметры печати
        print_time, mass_g, volume_cm3 = process_gcode(gcode_file_path)

        time_in_hours = f'{print_time // 60} час(-ов) {print_time % 60} минут'

        cost = (mass_g * 7) + (print_time // 60) * 10
        
        response = (f"Файл от {user_name}.\n"
                    f"Объём использованного пластика: {volume_cm3:.2f} см³\n"
                    f'Количество пластика: {mass_g:.2f} г\n'
                    f"Примерное время печати: {time_in_hours}\n"
                    f"Ориентировочная стоимость: {cost:.2f} рублей")

        await message.reply_photo(photo=open(image_path, 'rb'), caption=response)

        context.user_data['volume'] = volume_cm3
        context.user_data['mass'] = mass_g
        context.user_data['print_time'] = print_time
        context.user_data['cost'] = cost
        context.user_data['file_path'] = file_path
        context.user_data['image_path'] = image_path

        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data='confirm_yes'),
                InlineKeyboardButton("Нет", callback_data='confirm_no'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text("Вы хотите отправить информацию инженеру?", reply_markup=reply_markup)

    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        await message.reply_text(f"Произошла ошибка: {str(e)}")
