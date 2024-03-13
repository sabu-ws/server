#!/bin/bash

SERVICE_NAME=$1
SERVICE_UPTIME=$(systemctl status sabu.service | grep 'Active:' | cut -d';' -f2 | xargs)
echo $SERVICE_UPTIME
