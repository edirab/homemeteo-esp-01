#!/usr/bin/python3

import config
import logging
import sqlite3
from time import ctime, time
from datetime import datetime, timedelta

from meteostat import Parsel, datetime_to_timestamp, setup
from meteostat import plot_temp_hum, plot_soil, plot_lum, statistics_for_period

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

#DATABASE_FILE = '/home/pi/homemeteo-esp-01/mqtt.sqlite3'
DATABASE_FILE = '/mnt/d/PycharmProjects/arduino/esp-mosquitto/mqtt.sqlite3'

print("[bot] Starting HomeMeteo bot script at ", ctime(time()) )
db_conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
print("[bot] Connected to DB ", DATABASE_FILE)

def prettify(row):

    row = list(row[0])
    str_ =\
"""
T:    {} *C
H:    {} %
Soil: {}
Lum:  {}, {}
Time: {}
"""
      
    str_ = str_.format( row[1], row[2], row[3], row[4], row[5], datetime.fromtimestamp(row[6]) )
    return str_


def start(update: Update, context: CallbackContext):
    resp = """
List of commands:
/start  - display this message
/recent - get most recent data from database
/daily  - plot T, H, S and Lum for today
/daily dd.mm - plot stats for a period [dd.mm, today]
"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
    return


def help(update: Update, context: CallbackContext):
    resp = """
List of commands:
/start  - display this message
/recent - get most recent data from database
/daily  - plot T, H, S and Lum for today
/daily dd.mm - plot stats for a period [dd.mm, today]
"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
    return


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    context.bot.send_dice(chat_id=update.effective_chat.id)
    return


def recent(update: Update, context: CallbackContext):

    print("[bot] recent callback")
    sql = "SELECT * FROM sensors_data WHERE ID = (SELECT MAX(ID)  FROM sensors_data);"
    cursor = db_conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    cursor.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text= prettify(row))
    return


def daily(update: Update, context: CallbackContext):
    params = update.message.text.split()
    cursor = db_conn.cursor()
    setup()

    if len(params) == 1:

        a = datetime.now()
        day_now = (a.day, a.month, a.year)
        b = a + timedelta(days=1)
        day_tomorrow = (b.day, b.month, b.year)
        
        statistics_for_period( day_now, day_tomorrow,  cursor)

    elif len(params) == 2:
        begin_date = params[1].split('.')
        day_begin = (int(begin_date[0]), int(begin_date[1]), 2022)
        a = datetime.now()
        day_now = (a.day, a.month, a.year)
        statistics_for_period(day_begin, day_now, cursor)


    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('/run/user/1000/1.jpg', 'rb'))
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('/run/user/1000/2.jpg', 'rb'))
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('/run/user/1000/3.jpg', 'rb'))
    return



def main():



    updater = Updater(token=config.TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)



    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    recent_handler = CommandHandler('recent', recent)
    daily_handler = CommandHandler('daily', daily)
    help_handler = CommandHandler('help', help)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(recent_handler)
    dispatcher.add_handler(daily_handler)
    dispatcher.add_handler(help_handler)

    updater.start_polling()
    return


if __name__ == '__main__':
    main()
