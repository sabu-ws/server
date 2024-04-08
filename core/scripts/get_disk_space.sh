#!/bin/sh

DF_SYS=$(df / --output=used,avail | tail -n 1 | awk '{print $1,$2}' | tr -d 'G' | tr -d 'K')
echo $DF_SYS  # return used, availaible

DATA=$(grep "DATA_PATH" /sabu/server/.env | cut -d'=' -f2 | tr -d '"')
DF_DATA=$(df $DATA --output=used,avail | tail -n 1 | awk '{print $1,$2}' | tr -d 'G' | tr -d 'K')
echo -n $DF_DATA # return used, availaible