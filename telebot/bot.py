#!/usr/bin/python3

import config
import logging
import sqlite3
from time import ctime, time
from datetime import datetime

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
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    return


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
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
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('../imgs/1.jpg', 'rb'))
    context.bot.send_message(chat_id=update.effective_chat.id, text=str(params))
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

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(recent_handler)
    dispatcher.add_handler(daily_handler)

    updater.start_polling()
    return


if __name__ == '__main__':
    main()
