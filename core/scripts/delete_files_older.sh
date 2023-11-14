# SABU-SERVER
#!/bin/bash

remove="false"

while getopts p:d:r: flag
do
    case "${flag}" in
        p) path=${OPTARG};;
        d) day=${OPTARG};;
        r) remove=${OPTARG};;
    esac
done

if [[ "$day" =~ ^[0-9]+$ ]];
then

    if [ "$remove" == "false" ];
    then

        echo "[*] List files older than $days days from $path"
        find $path -type f -mtime +$day -printf "%t %p\n"


    elif [ "$remove" == "true" ];
    then

        echo "[*] Remove files older than $days days from $path"
        find $path -type f -mtime +$day -printf "%t -%p\n" -delete

    else

        echo "$0 -p <str:PATH> -d <int:DAYS> [-r <bool: true/false]"
        exit 1
    fi

else

    echo "$0 -p <str:PATH> -d <int:DAYS> [-r <bool: true/false]"
    exit 1
fi


