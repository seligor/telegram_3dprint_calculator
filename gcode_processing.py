from loguru import logger

def process_gcode(gcode_file_path):
    logger.info('Запущена обработка G-code')
    print_time = None
    mass_g = None
    volume_cm3 = None

    try:
        with open(gcode_file_path, 'r') as file:
            for line in file:
                if line.startswith("; filament used [g]"):
                    parts = line.split("=")
                    if len(parts) > 1:
                        mass_str = parts[1].strip()
                        mass_g = float(mass_str)
                        logger.info(f'Масса филамента: {mass_g} г')

                if line.startswith("; filament used [cm3]"):
                    parts = line.split("=")
                    if len(parts) > 1:
                        volume_str = parts[1].strip()
                        volume_cm3 = float(volume_str)
                        logger.info(f'Объём филамента: {volume_cm3} см³')


                if line.startswith("; estimated printing time"):
                    parts = line.split("=")
                    if len(parts) > 1:
                        time_str = parts[1].strip()
                        print_time = parse_time_string(time_str)

    except FileNotFoundError:
        logger.error("Файл G-code не найден.")

    return print_time, mass_g, volume_cm3

def parse_time_string(time_str):
    hours = 0
    minutes = 0
    parts = time_str.split()
    for part in parts:
        if 'h' in part:
            hours = int(part.replace('h', ''))
        elif 'm' in part:
            minutes = int(part.replace('m', ''))
    logger.info(f'Время печати составляет {hours}h {minutes}m, возвращаем {hours * 60 + minutes}')
    return hours * 60 + minutes
