#!/usr/bin/python3

from datetime import datetime
from time import sleep
from time import time
from time import ctime

from tempfile import tempdir
import paho.mqtt.client as mqtt
import sqlite3



def main():
    x = datetime.now()
    f = open("/tmp/dbg_cron.log", "w")
    print("Starting debug script at", x)
    
    while True:
        x = datetime.now()
        str_ = str(x) + '\n'
        print(str_, end='')
        f.write(str_)
        sleep(1)

if __name__ == "__main__":
    main()
