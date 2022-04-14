
- [Задать пароль и пользователя для брокера mosquitto](http://www.steves-internet-guide.com/mqtt-username-password-example/)

- Откуда взят [mqtt_test.py](https://lindevs.com/save-mqtt-data-to-sqlite-database-using-python/)

Чтобы подключиться извне к mqtt-рокеру mosquitto нужно 
добавить конфигурацию my.conf в `/etc/mosquitto/conf.d/`

- Команды для теста:

	mosquitto_sub -d -t hello/world
	mosquitto_pub -d -t hello/world -m "Hello from Terminal window 2!"


### Настройка VS Code для работы с Arduino

- Установить плагин Arduino
- Прописать путь к библиотекам, устанавливаемым через менеджер: 
	`corsair2\\Documents\\Arduino\\libraries` в `arduino.json`
- Добавить параметр `"output": "build"` в `arduino.json`


### Заметки
- Логин пароль `esp/esp`


### Процесс разработки

[+] Устанока и настройка mqtt-брокера на Raspberry Pi
[+] Поиск/проверка скрипта на python для записи данных, полученных от брокера
[+]  Разработка тестового ПО для ESP-01 для отладки приёма данных. Посылка миллисекунд с момента включения
[] Определиться что будем использовать: 
	- ардуино в связке в esp 01, 
	- nodemcu v3
	- esp 01 itself

	Для этого нужно определиться с составом датчиков. Берём
	- DHT 22 (влажность/температура)
	- Влажность почвы (аналоговый вход)
	- Пара фоторезисторов (аналоговые входы)
[] Разработать формат посылки. Такой вариант:

`Soil: 100 Lum: 456 645\n`
`100 456 654`