#!/usr/bin/python3

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
N_RECORDS = 5 * 60
DATABASE_FILE = 'mqtt.db'

messages = []
 
def on_connect(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(TOPIC)
 

def create_records(user_data):

    if len(messages) > N_RECORDS:

        sql = 'INSERT INTO sensors_data (topic, payload, created_at) VALUES (?, ?, ?)'
        records = []

        for msg in messages:
            payload = msg.payload.decode('utf-8')
            print("on_message", msg.topic, " : ", payload)
            record = (msg.topic, payload, int(time()))
            records.append(record)
            # print("\n")

        db_conn = user_data['db_conn']
        
        cursor = db_conn.cursor()
        cursor.executemany(sql, records)
        db_conn.commit()
        cursor.close()

        messages.clear()


def on_message(mqtt_client, user_data, message):

    messages.append(message)
    create_records(user_data)


def main():
    db_conn = sqlite3.connect(DATABASE_FILE)
    sql = """
    CREATE TABLE IF NOT EXISTS sensors_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        payload TEXT NOT NULL,
        created_at INTEGER NOT NULL
    )
    """
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