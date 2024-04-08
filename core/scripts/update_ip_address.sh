#!/bin/bash

INTERFACE_FILE="/etc/network/interfaces"
DNS_FILE="/etc/resolv.conf"

while getopts ":i:a:n:g:1:2:" opt
do
    case $opt in
        i)  INTERFACE_NAME=$OPTARG
            ;;
        a)
            INTERFACE_ADDRESS=$OPTARG
            ;;
        n)
            INTERFACE_NETMASK=$OPTARG
            ;;
        g)
            INTERFACE_GATEWAY=$OPTARG
            ;;
        1)
            DNS_1=$OPTARG
            ;;
        2)
            DNS_2=$OPTARG
            ;;
    esac
done

if [ -z "$INTERFACE_NAME" ] || [ -z "$INTERFACE_ADDRESS" ] || [ -z "$INTERFACE_NETMASK" ] || [ -z "$INTERFACE_GATEWAY" ] || [ -z "$DNS_1" ] || [ -z "$DNS_2" ]
then    
    echo "$0 -i <str:INTERFACE_NAME> -a <ipv4:ADDRESS> -n <ipv4:NETMASK> -g <ipv4:GATEWAY> -1 <ipv4:DNS_PRIMARY> -2 <ipv4:DNS_SECONDARY>"
    exit 1
fi

if [ ! -f "$INTERFACE_FILE" ]
then
    echo "File doesn't exist"
    exit 1
fi

if [ ! -f "$DNS_FILE" ]
then
    echo "File doesn't exist"
    exit 1
fi

sed -i -e "/^iface ${INTERFACE_NAME}/,/^\s*$/ s/address .*/address ${INTERFACE_ADDRESS}/" $INTERFACE_FILE
sed -i -e "/^iface ${INTERFACE_NAME}/,/^\s*$/ s/netmask .*/netmask ${INTERFACE_NETMASK}/" $INTERFACE_FILE
sed -i -e "/^iface ${INTERFACE_NAME}/,/^\s*$/ s/gateway .*/gateway ${INTERFACE_GATEWAY}/" $INTERFACE_FILE

sed -i -e "1s/nameserver .*/nameserver ${DNS_1}/" $DNS_FILE
sed -i -e "2s/nameserver .*/nameserver ${DNS_2}/" $DNS_FILE

systemctl restart networking
