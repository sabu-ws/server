# SABU-SERVER
#!/bin/bash

#used=$(vmstat | tail -1 | awk '{print $4}')
used=$(vmstat -s | head -n 2 | tail -n 1 | awk '{print $1}')
total=$(vmstat -s | head -n 1 | awk '{print $1}')
echo $used $total # used total
