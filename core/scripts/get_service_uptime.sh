#!/bin/bash

SERVICE_NAME=$1
SERVICE_UPTIME=$(systemctl status ${SERVICE_NAME} | grep 'Active:' | cut -d';' -f2 | xargs)
echo $SERVICE_UPTIME
