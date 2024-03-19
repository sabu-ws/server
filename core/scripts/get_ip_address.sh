#!/bin/bash

INTERFACE_NAME=$1

INTERFACE_FILE="/etc/network/interfaces"
DNS_FILE="/etc/resolv.conf"

INTERFACE_ADDRESS=$(grep "auto ${INTERFACE_NAME}" -A4 $INTERFACE_FILE | grep address| awk '{print $2}')
INTERFACE_NETMASK=$(grep "auto ${INTERFACE_NAME}" -A4 $INTERFACE_FILE | grep netmask| awk '{print $2}')
INTERFACE_GATEWAY=$(grep "auto ${INTERFACE_NAME}" -A4 $INTERFACE_FILE | grep gateway| awk '{print $2}')

DNS_1=$(awk 'NR==1 {print}' $DNS_FILE | awk '{print $2}')
DNS_2=$(awk 'NR==2 {print}' $DNS_FILE | awk '{print $2}')

echo -e "${INTERFACE_ADDRESS}\n${INTERFACE_NETMASK}\n${INTERFACE_GATEWAY}\n${DNS_1}\n${DNS_2}"
