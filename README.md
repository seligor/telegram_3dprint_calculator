# telegram_3dprint_calculator
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


Запуск


```python bot_interface.py```
