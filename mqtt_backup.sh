#!/bin/bash

# To get this UUID, run this command: 
#   sudo ls -l /dev/disk/by-uuid/

# Create mount point:
#   sudo mkdir /media/pi/adata
#   sudo chown pi:pi /media/pi/adata
#   sudo chmod 755   /media/pi/adata

# Edit fstab to auto moun flash drive:
#   sudo nano fstab
#   UUID=FEE2-F6EB /media/pi/adata vfat uid=pi,gid=pi,utf8  0 0

# Add permissions
#   sudo chmod 755 mqtt_backup.sh

# Add task to crontab to run once a day
# sudo crontab -e
# 17 13 * * * /home/pi/Documents/mqtt_backup.sh

rm /media/pi/adata/homemeteo-esp-bak/*.bak
mv /media/pi/adata/homemeteo-esp-bak/mqtt.sqlite3 /media/pi/adata/homemeteo-esp-bak/mqtt.sqlite3.bak

cp /home/pi/homemeteo-esp-01/mqtt.sqlite3  /media/pi/adata/homemeteo-esp-bak/
