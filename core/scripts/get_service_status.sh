# SABU-SERVER
#!/bin/bash

SERVICE_NAME=$1
SERVICE_STATUS=$(systemctl is-active $SERVICE_NAME | grep -E "[a-z]+")

if [[ $SERVICE_STATUS == "active" ]];
then
    SERVICE_TIMESTAMP=$(systemctl show -p ActiveEnterTimestamp $SERVICE_NAME --value)
    SERVICE_RUNTIME=$(( ( $(date +%s) - $(date -d "$SERVICE_TIMESTAMP" +%s) ) / 60 ))

    echo "SERVICE_NAME:$SERVICE_NAME\nSTATUS:$SERVICE_STATUS\nRUNTIME:$SERVICE_RUNTIME"

elif [[ $SERVICE_STATUS == "inactive" ]];
then
    echo "SERVICE_NAME: $SERVICE_NAME; STATUS: $SERVICE_STATUS;"
fi
