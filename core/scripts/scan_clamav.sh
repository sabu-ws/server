#!/bin/bash

while getopts ":s:q:l:" opt
do
    case $opt in
        s)  SCAN_PATH=$OPTARG
            ;;
        q)
            QUARANTINE_PATH=$OPTARG
            ;;
        l)
            LOG_PATH=$OPTARG
            ;;
    esac
done

if [ -z "$SCAN_PATH" ] || [ -z "$QUARANTINE_PATH" ] || [ -z "$LOG_PATH" ]
then    
    echo "$0 -s <str:SCAN_PATH> -q <str:QUARANTINE_PATH> -l <str:LOG_PATH>"
    exit 1
fi

# VARS
TIMESTAMP=$(date +%s)
LOG_NAME="${LOG_PATH}/clamav_${TIMESTAMP}.log"

# SCAN
clamscan --recursive=yes --log=$LOG_NAME --move=$QUARANTINE_PATH $SCAN_PATH
SCAN_STATUS=$?

# RESULT
echo -n "${LOG_NAME};${SCAN_STATUS}"
