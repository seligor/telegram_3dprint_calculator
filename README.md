# telegram_3dprint_calculator
![Static Badge](https://img.shields.io/badge/seligor-telegram_3dprint_calculator-telegram_3dprint_calculator)
![GitHub top language](https://img.shields.io/github/languages/top/seligor/telegram_3dprint_calculator)
![GitHub issues](https://img.shields.io/github/issues/seligor/telegram_3dprint_calculator)



Бот, который в автоматическом режиме строит модель из stl файла и обсчитывает количество пластика и затраченное время. На основе этого рассчитывает стоимость изготовления детали

Скачивание

```git clone https://github.com/seligor/telegram_3dprint_calculator.git```

Установка

```python3 -m venv venv```

```cat prusa-slicer-bin.zip* > prusa-slicer-bin.zip```

```unzip prusa-slicer-bin.zip```

```chmod a+x ./prusa-slicer```

```rm -f prusa-slicer-bin*```

Если по какой либо причине prusa-slicer у вас не запустился - вас ждёт увлекательный процесс сборки своей версии консольного слайсера
https://github.com/prusa3d/PrusaSlicer/issues/7521


Активация окружения

```source venv/bin/activate```

Установка библиотек

```pip install -r requirements.txt```


Настройка

```cp .env-dist .env```
отредактировать .env

Добавить профиль печати (файл printer_profile/PRINTER.ini)

Для простой генерации конфига накидал скрипт, который собирает парамеры и записывыает в PRINTER.ini. 
Вам потребуется: 
1. создать папку incoming
2. поместить в неё настройки печати из папок

```
   %APPDATA%/PrusaSlicer/filament
   %APPDATA%/PrusaSlicer/print
   %APPDATA%/PrusaSlicer/printer
```

3. Выбирайте для генерации конфига те же профили, которые используете, не надо закидывать все
4. Запустите программу и она сгенерирует PRINTER.ini

Запуск


```python bot_interface.py```
