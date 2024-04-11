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
LOG_NAME="${LOG_PATH}/oletools_${TIMESTAMP}.log"

# SCAN
for FILE in $(find $SCAN_PATH -type f)
do
    FILE_FORMAT=$(oleid $FILE | grep "Container format" | cut -d'|' -f2 | tr -d ' ')

    if [ "$FILE_FORMAT" = "OLE" ]
    then
        FILE_MACRO=$(oleid $FILE | grep -E "VBA Macros|XML Macros" | cut -d'|' -f2 | tr -d ' ')

        if [ "$FILE_MACRO" = "Yes,suspicious" ]
        then
            echo "[MALICIOUS] $FILE" >> $LOG_PATH/$LOG_NAME
            mv $FILE $QUARANTINE_PATH
        fi
    fi
done


# RESULT
echo "${LOG_NAME};${SCAN_STATUS}"
