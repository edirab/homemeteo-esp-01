## Проект домашней метеостанции на ESP-01 и Arduino

![]()
![]()

### О проекте:

Устройство раз в 2 секунды собирает данные о 
- температуре, 
- влажности воздуха, 
- влажности почвы и 
- относительной освещённости в двух точках 

Пакет по локальной сети через wifi отправляется MQTT-брокеру `mosquitto`, развёрнутом на `Raspberry Pi 3B`. Скрипт `mqtt_test.py`, который обработывает callback от брокера, накапливает данные, добавляет к ним временную метку и раз в 10 минут производит запись в базу данных.

Раз в сутки производится резервное копирование БД на флешку.
За день накапливается ~1,7 Mb

Собранные данные можно проанализировать и определить, например, 
- частоту полива цветка
- изменения температуры и влажности воздуха с временами года,
- изменение освещённости в течение дня и в течение года
- оценить продолжительность светового дня
( в том числе и во сколько автор ложится спать :) )


### Цели проекта: 

- освоить микроконтроллер `ESP 8266` в его проестейшей версии `ESP 01`
- познакомиться с протоколом MQTT
- реализовать надёжную двунаправленную связь по UART между микроконтроллерами на основе протокола с подтверждением
- углубить познания в отладке `cron`


### Состав репозитория

- Скетч `meteo.ino` для Arduino
- Скетч `esp_test.ino` для ESP-01
- Python-скрипт `mqtt_test.py`
- `bash`-скрипт для резервного копирования
- Проект KiCad 6.0: 
    + схема электическая принципиальная
    + примерная компоновка печатной платы
    + Bill of materials
- фото устройства
- описание для настройки автозапуска

### Развёртывание ПО

1. Установить зависимости
```shell
sudo apt update && sudo apt upgrade
pip3 install pysqlite3
pip3 install paho-mqtt
pip3 install python-telegram-bot --upgrade
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service
```
2. Настроить `mqtt`-брокер
- отредактировать системный конфигурационный файл или
```shell
sudo nano /etc/mosquitto/mosquitto.conf
> listener 1883
> allow_anonymous true
```
- скопировать конфигурацию `my.conf`: `sudo cp <path_to_repo/my.conf> /etc/mosquitto/conf.d/`

3. `sudo reboot`
4. Проверка конфигурации брокера:
```shell
	mosquitto_sub -d -t hello/world
	mosquitto_pub -d -t hello/world -m "Hello from Terminal window 2!"
	mosquitto_sub -t home/#
```


### Настройка автозапуска приложения и резервного копирования

1. Устанавливаем права и запускаем вручную, чтобы создать первоначальный файл базы данных на флешке.
```shell
chmod +x *.sh
./mqtt_backup.sh
```
2. Редактируем таблицу `cron` от имени обычного пользователя. Явно добавляем переменные окружения, т.к. у `cron` они отличаются
```shell
crontab -e

SHELL=/bin/bash
HOME=/home/pi
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games	

@reboot 	 /usr/bin/python3 /home/pi/Documents/mqtt_test.py >> /home/pi/Documents/1.log &
# Каждый день в 15:50
50 15 * * *  /bin/bash  /home/pi/Documents/mqtt_backup.sh
```

3. Считываем заново таблицу
```shell
sudo service cron reload
```
4. Проверка автозапуска
```shell
sudo reboot
ps -ax | grep mqtt
```


#### Важно при настройке автозапуска по cron

1. Пути ко всем ресурсам как в `crontab`, так и внутри скрипта, лучше прописывать абсолютные
2. Ресурсы, к которым обраются скрипты, должны иметь соотв. права (БД и файл логов доступны для чтения/записи)
3. Использовать лучше таблицу для обычного пользователя, а не `root`, в противном случае придётся устанавливать все библиотеки и для root: `sudo pip3 install pysqlite3`
4. ! Формат записи: `# m h  dom mon dow   command` - сначала минуты!
5. Для отладки пользоваться гайдом [отсюда](https://stackoverflow.com/questions/22743548/cronjob-not-running)


### Процесс разработки

- [x] Устанока и настройка `mqtt`-брокера на Raspberry Pi
- [x] Поиск/проверка скрипта на python для записи данных, полученных от брокера
- [x] Разработка тестового ПО для ESP-01 для отладки приёма данных по MQTT. Например, посылка миллисекунд с момента включения
- [x] Определиться что будем использовать: ардуино в связке в esp 01

- [x] Для этого нужно определиться с составом датчиков. Берём
  + DHT 22 (влажность/температура)
  + Влажность почвы (аналоговый вход)
  + Пара фоторезисторов (аналоговые входы)
	
- [x] Разработать формат UART-посылки. Принят такой вариант:
	`27.2 35.6 3 456 645\r\n`

- [x] Разработать метод для разбора посылки на стороне esp 01, пришедшей по последовательному интерфейсу
- [x] Протестировать взаимодействие устройств на макетной плате -> Минимальное жизнеспособное приложение!
- [x] Добавить 3 светодиода на ардуино: 
  + красный для сигнализации о потере mqtt-соединения,
  + жёлтый - сухая почва цветка
  + зелёный для сигнализации о потере wifi-соединения,

- [x] Начертить схему электрическую принципиальную
- [x] Сделать компоновку печатной платы
- [x] Собрать устройство на паечной макетной плате

- [x] Необходимо разработать более надёжный протокол управления, основанный на сообщениях 
с уникальными префиксами и подтверждениями 

- [x] Доработать скрипт на python. Нельзя вести запись на карту памяти каждые 2 секунды.
	Слишком большой износ. Сделать раз в 3-5 минут
- [x] Изменить схему базы данных для более компактного хранения данных

- [ ] Добавить обработку ЖЁЛТОГО светодиода, подобрать пороговое значение для влажности почвы
- [ ] Оформить проект красиво: сделать фото устройства, составить Bill of Materials, сохранить в pdf схему эл. принц.

- [x] Разобраться как настроить автозапуск скрипта при старте Raspbian

- [x] Добавить `bash`-скрипт для резервного копирования БД на флешку раз в сутки по `cron`
- [ ] Сделать бота для Телеграм, чтобы можно было получить доступ к данным из любой точки мира с телефона. Продумать функционал

- [ ] Как насчёт добавить какой-либо пользовательский интерфейс для задания новых
  + логина/пароля для wifi-сети,
  + ip-адреса mqtt-брокера


### Заметки

- [Задать пароль и пользователя для брокера mosquitto](http://www.steves-internet-guide.com/mqtt-username-password-example/)

- Откуда взят [mqtt_test.py](https://lindevs.com/save-mqtt-data-to-sqlite-database-using-python/)


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

Единственный вариант - пропустить эти сообщения


### Отладка автозапуска

Способы настройки автозапуска
- rc.local
- init.d
- systemd
- cron
- .bashrc

##### 1. Скрипт dbg_cron.py

1.1 Для отладки запуска в cron по reboot создадим простой скрипт.
Просто выводим дату и время в файл

В crontab обычного пользователя добавим 
	@reboot /usr/bin/python3 /home/pi/Documents/dbg_cron.py

- Просмотр изменений файла:
	watch -n 1 tail -1 /tmp/dbg_cron.log
	sudo tail -n20 -f /var/log/mosquitto/mosquitto.log
	sudo cp /home/pi/Documents/mymqttclient.service /etc/systemd/system/

=====

cat /var/log/syslog | grep cron
cat /var/log/syslog | grep CRON
tail -f /var/log/syslog
