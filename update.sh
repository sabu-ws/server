#!/bin/bash

# STOP SABU SERVICE
systemctl stop sabu.service >/dev/null

# CHECK SABU IMAGES
if [ -e /sabu/server/ProfilePicture/ ]
then
    cp -r /sabu/server/ProfilePicture /tmp/ >/dev/null

else
    echo "ERROR: Picture"
fi

# UPDATE SOURCES
cd /sabu/server
git config --global --add safe.directory /sabu/server
git pull

# UPDATE VENV
source /sabu/sabu-venv/bin/activate >/dev/null
pip3 install -r /sabu/server/requirements.txt >/dev/null
flask db upgrade

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
