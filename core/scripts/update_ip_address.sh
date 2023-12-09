# SABU-SERVER
#!/bin/bash

INTERFACE_FILE="/etc/network/interfaces"

while getopts ":i:a:n:g:" opt
do
    case $opt in
        i) INTERFACE_NAME=$OPTARG
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
    esac
done

if [ -z "$INTERFACE_NAME" ] || [ -z "$INTERFACE_ADDRESS" ] || [ -z "$INTERFACE_NETMASK" ] || [ -z "$INTERFACE_GATEWAY" ]
then
    echo "$0 -i <str:INTERFACE_NAME> -a <ipv4:ADDRESS> -n <ipv4:NETMASK> -g <ipv4:GATEWAY>"
    exit 1
fi

if [ ! -f "$INTERFACE_FILE" ]
then
    echo "File doesn't exist"
    exit 1
fi

sed -i -e "/^iface ${INTERFACE_NAME}/,/^\s*$/ s/address .*/address ${INTERFACE_ADDRESS}/" "$INTERFACE_FILE"
sed -i -e "/^iface ${INTERFACE_NAME}/,/^\s*$/ s/netmask .*/netmask ${INTERFACE_NETMASK}/" "$INTERFACE_FILE"
sed -i -e "/^iface ${INTERFACE_NAME}/,/^\s*$/ s/gateway .*/gateway ${INTERFACE_GATEWAY}/" "$INTERFACE_FILE"

systemctl restart networking
