### Проект домашней метеостанции на ESP-01 и Arduino

![]()
![]()

#### О проекте:

Устройство раз в 2 секунды собирает данные о 
- температуре, 
- влажности воздуха, 
- влажности почвы и 
- относительной освещённости в двух точках 

и через локальную сеть отправляет MQTT-брокеру, развёрнутом на Raspberry Pi 3B.
На Raspberry Pi работает скрипт `mqtt_test.py`, который обработывает callback от брокера, накапливает
данные, добавляет к ним временную метку и раз в 5-10 минут производит запись в базу данных.

Собранные данные можно проанализировать и определить, например, 
- частоту полива цветка
- изменения температуры и влажности воздуха с временами года,
- изменение освещённости в течение дня и в течение года
( в том числе и во сколько автор ложится спать :) )


### Состав репозитория

- Скетч `meteo.ino` для Arduino
- Скетч `esp_test.ino` для ESP-01
- Python-скрипт `mqtt_test.py`
- Проект KiCad 6.0: схема электическая принципиальная и примерная компоновка печатной платы


#### Цели проекта: 

- освоить микроконтроллер ESP 8266 в его проестейшей версии ESP 01
- познакомиться с протоколом MQTT
- реализовать двунаправленную связь по UART между микроконтроллерами


### Процесс разработки

- [+] Устанока и настройка mqtt-брокера на Raspberry Pi
- [+] Поиск/проверка скрипта на python для записи данных, полученных от брокера
- [+] Разработка тестового ПО для ESP-01 для отладки приёма данных по MQTT. Например, посылка миллисекунд с момента включения
- [+] Определиться что будем использовать: ардуино в связке в esp 01

- [+] Для этого нужно определиться с составом датчиков. 
		Берём
		+ DHT 22 (влажность/температура)
		+ Влажность почвы (аналоговый вход)
		+ Пара фоторезисторов (аналоговые входы)
	
- [+] Разработать формат посылки. Принят такой вариант:
	`27.2 35.6 3 456 645\r\n`

- [+] Разработать метод для разбора посылки на стороне esp 01, пришедшей по последовательному интерфейсу
- [+] Протестировать взаимодействие устройств на макетной плате -> Минимальное жизнеспособное приложение!
- [+] Добавить 3 светодиода на ардуино: 
		- красный для сигнализации о потере mqtt-соединения,
		- жёлтый - сухая почва цветка
		- зелёный для сигнализации о потере wifi-соединения,

- [+] Начертить схему электрическую принципиальную
- [+]	Сделать компоновку печатной платы
- [+] Собрать устройство на паечной макетной плате

- [+] Необходимо разработать более надёжный протокол управления, основанный на сообщениях 
с уникальными префиксами и подтверждениями 

- [+] Доработать скрипт на python. Нельзя вести запись на карту памяти каждые 2 секунды.
	Слишком большой износ. Сделать раз в 3-5 минут
- [+] Изменить схему базы данных для более компактного хранения данных

- [ ] Добавить обработку ЖЁЛТОГО светодиода, подобрать пороговое значение для влажности почвы
- [ ] Оформить проект красиво: сделать фото устройства, составить Bill of Materials, сохранить в pdf схему эл. принц.

- [ ] Разобраться как настроить автозапуск скрипта при старте Raspbian
		@reboot sleep 10 && /home/pi/Documents/mqtt_test.py &> /dev/null &
		@reboot sleep 10 && /usr/bin/python /home/pi/Documents/mqtt_test.py &> /home/pi/Documents/log.txt &

- [ ] Добавить bash-скрипт для резервного копирования БД на флешку раз в сутки по cron
- [ ] Как насчёт добавить какой-либо пользовательский интерфейс для задания новых
		логина/пароля для wifi-сети,
		ip-адреса mqtt-брокера


### Заметки

- [Задать пароль и пользователя для брокера mosquitto](http://www.steves-internet-guide.com/mqtt-username-password-example/)

- Откуда взят [mqtt_test.py](https://lindevs.com/save-mqtt-data-to-sqlite-database-using-python/)

Чтобы подключиться извне к mqtt-рокеру mosquitto нужно 
добавить конфигурацию my.conf в `/etc/mosquitto/conf.d/`
```
	listener 1883
	allow_anonymous true
```
- Команды для теста:

```
	mosquitto_sub -d -t hello/world
	mosquitto_pub -d -t hello/world -m "Hello from Terminal window 2!"
	mosquitto_sub -t home/#
```

### Настройка VS Code для работы с Arduino

- Установить плагин Arduino
- Прописать путь к библиотекам, устанавливаемым через менеджер: 
	`corsair2\\Documents\\Arduino\\libraries` в `arduino.json`
- Добавить параметр `"output": "build"` в `arduino.json`



- Логин пароль `esp/esp`

### Bootloader debug messages

При загрузке esp выкидывает в uart отладочную информацию о работе загрузчика.
Поделать с этим ничего нельзя, только проигнорировать.
Скорость baudrate 74800 bit/s

Для отключения подобного вывода необходимо GPIO 15 (MTDO) [притянуть к нулю](https://www.esp32.com/viewtopic.php?t=10597) ,
но на ESP-01 вывод не разведён

```
	Posting for someone who still needs help on this topic.
	[Note: I'm using IDFv4.4 dev]

	Step1: got to menuconfig -> component config -> esp system settings -> channel for console output
	Set to - Custom UART
	Come one level behind and you'll find new options: UART peripheral to use for console output
	Set this to UART1
	You may also change the pins for UART0/1 that you are using now, by writing them in "UART Tx in GPIO# " option,
	if you want to use UART0 pins (Tx-GPIO1 & Rx-GPIO3) for other purposes or simply change their respective pins to somewhere more convenient while designing a complex PCB.

	Now, save and quit menuconfig -> flash operation is always done through UART0 (GPIO 1&3) but monitoring can now be done through UART1
	However, on every reset (POWER_ON/SW_RESET/WDT_RESET, etc.) the UART0 pins will output bootloader logs even-though they are supposed to be printed through UART1. For this, I tried setting BOOTLOADER and LOGOUTPUT to NONE in menuconfig, but it only stopped printing the respective logs on UART1 (coz. we had set it that way).

	The real solution is to pulldown GPIO15 so that even those bootup logs at UART0 can be stopped and now you're free to use the GPIO 1&3 for I/O operations.
```

Единственный вариант - пропустить эти сообщения. Подключим вывод RST к ардуино



