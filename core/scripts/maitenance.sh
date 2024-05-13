#!/bin/bash

# SYSTEM UPDATE/UPGRADE
apt update
apt upgrade -y

# UPDATE TIMESCALE
timescaledb-tune --quiet --yes

# UPDATE CLAMAV DATABASE
systemctl stop clamav-freshclam.service
freshclam
systemctl start clamav-freshclam.service
