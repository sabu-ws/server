#!/bin/sh

DF_SYS=$(df -h / --output=used,avail | tail -n 1 | awk '{print $1,$2}' | tr -d 'G' | tr -d 'K')
echo $DF_SYS  # return used, availaible

DATA=$(grep "DATA_PATH" /sabu/server/.env | cut -d'=' -f2 | tr -d '"')
DF_DATA=$(df -h $DATA --output=used,avail | tail -n 1 | awk '{print $1,$2}' | tr -d 'G' | tr -d 'K')
echo $DF_DATA # return used, availaible