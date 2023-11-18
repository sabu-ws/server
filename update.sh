#!/bin/bash

while getopts :b: flag
do
        case "${flag}" in
                b) BRANCH=${OPTARG};;
        esac
done

# STOP SABU SERVICE
systemctl stop sabu.service >/dev/null

# CHECK SABU DATABASE
if [ -e /sabu/server/instance/database.db ]
then
    cp -r /sabu/server/instance/ /tmp/ >/dev/null

else
    echo "ERROR: Database"
fi

# CHECK SABU IMAGES
if [ -e /sabu/server/ProfilePicture/ ]
then
    cp -r /sabu/server/ProfilePicture /tmp/ >/dev/null

else
    echo "ERROR: Picture"
fi

# REMOVE OLD SOURCES
rm -rf /sabu/server/ >/dev/null

# CLONE REPO
cd /sabu/
if [[ "$BRANCH" == "dev" ]];
then
    echo "CLONE: Dev"
    git clone https://github.com/sabu-ws/server.git -b dev -q >/dev/null

else
    echo "CLONE: Main"
    git clone https://github.com/sabu-ws/server.git -q >/dev/null

fi

# UPDATE VENV
source /sabu/sabu-venv/bin/activate >/dev/null
pip3 install -r /sabu/server/requirements.txt >/dev/null

# CHECK SABU DATABASE
if [ -e /tmp/instance/database.db ]
then
    cp -r /tmp/instance/ /sabu/server/  >/dev/null

else
    echo "ERROR: Database"
fi

# CHECK SABU IMAGES
if [ -e /tmp/ProfilePicture/ ]
then
    cp -r /tmp/ProfilePicture/ /sabu/server/ >/dev/null

else
    echo "ERROR: Picture"
fi

# UPDATE PERMISSIONS
chmod -R 0750 /sabu/ >/dev/null
chown -R svc-sabu:svc-sabu /sabu/ >/dev/null

# START SABU SERVICE
systemctl start sabu.service >/dev/null

# CHECK SABU SERVICE
COMMAND=$(systemctl status sabu.service)
STATUS=$?

if [ $STATUS -eq 0 ]
then
    echo "SABU: Updated"

else
    echo "ERROR: Start service" 
fi
