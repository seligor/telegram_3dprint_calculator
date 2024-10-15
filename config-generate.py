import os

def read_and_sort_ini_files(input_dir, output_file):
    all_parameters = {}

    # Чтение всех INI-файлов из указанной директории
    for filename in os.listdir(input_dir):
        if filename.endswith('.ini'):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    # Пропускаем комментарии и пустые строки
                    if line.startswith('#') or not line:
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        all_parameters[key.strip()] = value.strip()

    # Сортируем параметры в алфавитном порядке
    sorted_parameters = dict(sorted(all_parameters.items()))

    # Записываем отсортированные параметры в новый файл
    with open(output_file, 'w') as output:
        output.write('# Sorted parameters\n')
        for key, value in sorted_parameters.items():
            output.write(f'{key} = {value}\n')

# Путь к директории с входными INI-файлами и имя выходного файла
input_directory = 'Incoming'
output_file_path = 'printer_profile/PRINTER.ini'

# Создаем директорию для выходного файла, если она не существует
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Выполняем функцию
read_and_sort_ini_files(input_directory, output_file_path)

print(f'Параметры успешно отсортированы и сохранены в {output_file_path}')
