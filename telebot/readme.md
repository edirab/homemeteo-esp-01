### Configuring bot


Список команд
start - запустить бота
help - вывести список команд
recent - получить последние данные
daily - статистика за сегодня


### Запуск бота в фоне и отвязка от консоли

```shell
	./bot.py &> /dev/null &
	disown <process-pid>
```


### TODO

- Выполнение команды /daily на RPI 3 занимает около 40 секунд, что слишком много.
Необходимо уменьшить выборку, скажем, до 300 точек

- Зафиксировать размер подмножества для одного графика. Скажем, 100 точек
- Сделать нормальные временные метки. Каждый час или каждые полчаса.
Зависит от диапазона измерений
