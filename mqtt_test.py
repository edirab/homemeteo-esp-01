#!/usr/bin/python3

from tempfile import tempdir
import paho.mqtt.client as mqtt
import sqlite3
from time import time
from time import ctime
from time import sleep
 
MQTT_HOST = '192.168.1.75'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'esp_1'
MQTT_USER = 'esp'
MQTT_PASSWORD = 'esp'
TOPIC = 'home/all'

# Запись в БД будет происходить каждые min * 60 s/min * 2 (минут), 
# т.к. посылка приходит раз в 2 секунды

N_RECORDS = 5 * 60
#N_RECORDS = 5
DATABASE_FILE = '/home/pi/Documents/mqtt.sqlite3'

messages = []


def on_connect(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(TOPIC)
 

def create_records(user_data):

    if len(messages) > N_RECORDS:

        sql = 'INSERT INTO sensors_data (temp, hum, soil, lum_1, lum_2, created_at) VALUES (?, ?, ?, ?, ?, ?)'
        # print(messages)
        print("Writing to DB at ", ctime(time()) )

        db_conn = user_data['db_conn']
        
        cursor = db_conn.cursor()
        cursor.executemany(sql, messages)
        db_conn.commit()
        cursor.close()
        messages.clear()


def on_message(mqtt_client, user_data, message):

    payload = message.payload.decode('utf-8')
    payload = str(payload).strip().split(' ')
    payload.append(int(time()))

    if (len(payload) >= 6):
        payload[0] = float( payload[0] )
        payload[1] = float( payload[1] )
        payload[2] = int( payload[2] )
        payload[3] = int( payload[3] )
        payload[4] = int( payload[4] )

    # print(payload)
    messages.append( tuple(payload) )
    create_records(user_data)


def main():
    sleep(20)
    print("Starting mqtt callback script at ", ctime(time()) )
    db_conn = sqlite3.connect(DATABASE_FILE)
    print("Connected to DB ", DATABASE_FILE)

    sql = """
    CREATE TABLE IF NOT EXISTS sensors_data (
        id         INTEGER PRIMARY KEY AUTOINCREMENT
                        NOT NULL,
        temp       REAL    NOT NULL,
        hum        REAL    NOT NULL,
        soil       INTEGER NOT NULL,
        lum_1      INTEGER NOT NULL,
        lum_2      INTEGER NOT NULL,
        created_at INTEGER NOT NULL
    );"""


    cursor = db_conn.cursor()
    cursor.execute(sql)
    cursor.close()
 
    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    print("Starting mqtt client")

    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.user_data_set({'db_conn': db_conn})
 
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
 
    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    print("Connected to mqtt client")
    mqtt_client.loop_forever()
    print("Looping forever")
 
 
main()