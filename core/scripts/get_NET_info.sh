#!/bin/bash

# Retrieve network informations
interface=$(ip -br a | awk '{print $1}' | grep -wv lo | head -n 1)
address=$(grep address /etc/network/interfaces | cut -d ' ' -f2)
netmask=$(grep netmask /etc/network/interfaces | cut -d ' ' -f2)
gateway=$(grep gateway /etc/network/interfaces | cut -d ' ' -f2)
nameserver1=$(grep -e "nameserver .*" /etc/resolv.conf | sed -n '1p')
nameserver2=$(grep -e "nameserver .*" /etc/resolv.conf | sed -n '2p')

# Display informations
echo -e "$interface\n$address\n$netmask\n$gateway\n$nameserver"

# --- Script By SABU --- #
