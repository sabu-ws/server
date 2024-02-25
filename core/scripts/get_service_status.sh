#!/bin/bash

SERVICE_NAME=$1
SERVICE_STATUS=$(systemctl is-active $SERVICE_NAME | grep -E "[a-z]+")

if [[ $SERVICE_STATUS == "active" ]];
then
    SERVICE_TIMESTAMP=$(systemctl show -p ActiveEnterTimestamp $SERVICE_NAME --value)
    SERVICE_TIMESTAMPER=$(date -d "$SERVICE_TIMESTAMP" +%s)

    echo -e "SERVICE_NAME: $SERVICE_NAME \nSTATUS: $SERVICE_STATUS\nRUNTIME: $SERVICE_TIMESTAMPER"

elif [[ $SERVICE_STATUS == "inactive" ]];
then
    echo -e "SERVICE_NAME: $SERVICE_NAME\nSTATUS: $SERVICE_STATUS"
fi
