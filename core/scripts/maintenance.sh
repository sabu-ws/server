#!/bin/bash

# NFTABLES MAINTENANCE
sh /sabu/server/core/scripts/filtering_maintenance.sh
sleep 3

# SYSTEM UPDATE/UPGRADE
apt update
apt upgrade -y

# UPDATE TIMESCALE
timescaledb-tune --quiet --yes

# UPDATE CLAMAV DATABASE
systemctl stop clamav-freshclam.service
freshclam
sleep 3
systemctl start clamav-freshclam.service

# NFTABLES PROD
sh /sabu/server/core/scripts/filtering_prod.sh
sleep 3

# LOG ACTION
date=$(date +"[%Y-%m-%d %H:%M:%S]")
echo "$date [SABU] The update script has been executed" >> /sabu/logs/server/sabu.log

# reboot
reboot