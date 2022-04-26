#!/usr/bin/python3

from tempfile import tempdir
import paho.mqtt.client as mqtt
import sqlite3
from time import time
 
MQTT_HOST = '192.168.1.75'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'esp_1'
MQTT_USER = 'esp'
MQTT_PASSWORD = 'esp'
TOPIC = 'home/#'

# В текущей реализации каждый параметр записывается отдельной строкой, 
# что есть неоптимально. Схема базы данных будет переработана в будущем
# Запись в БД будет происходить каждые 60 посылок, т.к. раз в 2 минуты
N_RECORDS = 5 * 5
DATABASE_FILE = 'mqtt.sqlite3'

messages = []

class Parsel:
    temp = 0
    hum = 0
    soil = 0
    lum_1 = 0
    lum_2 = 0



def on_connect(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(TOPIC)
 

def create_records(user_data):

    if len(messages) > N_RECORDS:

        sql = 'INSERT INTO sensors_data (temp, hum, soil, lum_1, lum_2, created_at) VALUES (?, ?, ?, ?, ?, ?)'
        records = []
        record = []

        first_elem = messages[0]
        while first_elem.topic != "home/temperature":
            messages.pop(0)
            first_elem = messages[0]

        for msg in messages:
            payload = msg.payload.decode('utf-8')

            if msg.topic == "home/temperature":

                if len(record):
                    records.append( tuple(record) )
                    print(record)
                    record.clear()

                record.append( float(payload) )

            elif msg.topic == "home/humidity":
                record.append( float(payload) )

            elif msg.topic == "home/soil":
                record.append( int(payload) )

            elif msg.topic == "home/lum1":
                record.append( int(payload) )

            elif msg.topic == "home/lum2":
                record.append( int(payload) )
                record.append(int(time()))

        print("records:")
        print(records)
        print("----")

        # records_tuples = list(map(tuple, records))
        # records_tuples = list(tuple(sub) for sub in records)

        # print(records_tuples)

        db_conn = user_data['db_conn']
        
        cursor = db_conn.cursor()
        cursor.executemany(sql, records)
        db_conn.commit()
        cursor.close()

        messages.clear()
        records.clear()
        record.clear()


def on_message(mqtt_client, user_data, message):

    messages.append(message)
    create_records(user_data)


def main():
    db_conn = sqlite3.connect(DATABASE_FILE)
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
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.user_data_set({'db_conn': db_conn})
 
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
 
    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    mqtt_client.loop_forever()
 
 
main()