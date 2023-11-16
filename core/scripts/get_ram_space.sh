# SABU-SERVER
#!/bin/bash

used=$(vmstat | tail -1 | awk '{print $4}')
total=$(vmstat -s | grep "total memory" | awk '{print $1}')
echo $used $total # used total
