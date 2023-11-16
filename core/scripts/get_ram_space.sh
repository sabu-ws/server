# SABU-SERVER
#!/bin/bash

used=$(vmstat | tail -1 | awk '{print $4}')
total=$(vmstat -s | grep "total memory" | awk '{print $1}')
echo $used $total
#DF=$(df -h / --output=used,avail | tail -n 1 | awk '{print $1,$2}' | tr -d 'G')
#echo $DF  # return used, availaible
