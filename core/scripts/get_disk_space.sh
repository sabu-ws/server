# SABU-SERVER
#!/bin/bash

DF=$(df -h / --output=used,avail | tail -n 1 | awk '{print $1,$2}' | tr -d 'G')
echo $DF  # return used, availaible
