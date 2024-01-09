# SABU-SERVER
#!/bin/bash

used=$(vmstat 1 2 | tail -1 | awk '{print $14}')
echo $used # used
