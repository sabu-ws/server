# SABU-SERVER
#!/bin/bash

while getopts n: flag
do
        case "${flag}" in
                n) NEW_HOSTNAME=${OPTARG};;
        esac
done

if [[ "$NEW_HOSTNAME" =~ ^[a-z0-9-]{5,63}$ ]];
then

        OLD_HOSTNAME=$(hostname -s)

        sed -i "s/$OLD_HOSTNAME/$NEW_HOSTNAME/g" /etc/hosts
        hostnamectl set-hostname $NEW_HOSTNAME

        sleep 5
        reboot
else
        echo "$0 -n <str:HOSTNAME>"
        exit 1
fi
