import os
import subprocess
import platform
from loguru import logger

def calculate_print_time(stl_file_path):
    # Определяем операционную систему
    current_os = platform.system()

    if current_os == "Windows":
        logger.info("ОС определена. Обнаружена Windows")
        prusa_slicer_path = r"C:\Program Files\Prusa3D\PrusaSlicer\prusa-slicer-console.exe"
    elif current_os == "Linux":
        logger.info("ОС определена. Обнаружена Linux")
        prusa_slicer_path = "./prusa-slicer"  # Предполагаем, что prusa-slicer доступен в PATH
    else:
        logger.error("Операционная система не поддерживается для автоматического расчета времени печати.")
        return None

    printer_profile_path = "./printer_profile/PRINTER.ini"
    output_dir = "./temp/"
    os.makedirs(output_dir, exist_ok=True)

    # Проверяем существование необходимых файлов
    if os.path.exists(prusa_slicer_path) and os.path.exists(printer_profile_path):
        logger.info("PrusaSlicer и профиль принтера обнаружены")

        # Создаем команду для запуска PrusaSlicer
        command = [
            prusa_slicer_path,
            "--export-gcode",
            stl_file_path,
            "--output",
            output_dir,
            "--load",
            printer_profile_path
        ]

        # Запускаем команду и ждем завершения
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            logger.info("G-code успешно создан")
            gcode_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(stl_file_path))[0] + ".gcode")
            return gcode_file_path
        else:
            logger.error(f"Ошибка при создании G-code: {result.stderr}")
    else:
        logger.error("PrusaSlicer или профиль принтера не найдены.")
        return None
