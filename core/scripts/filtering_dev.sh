#!/bin/bash

INTERFACE_NAME=$1

INTERFACE_FILE="/etc/network/interfaces"
DNS_FILE="/etc/resolv.conf"

if [ -z "$INTERFACE_NAME" ]
then
    echo "No interface specified"
    exit 1

else
    # GET DATA
    INTERFACE_ADDRESS=$(grep "auto ${INTERFACE_NAME}" -A4 $INTERFACE_FILE | grep address| awk '{print $2}')
    INTERFACE_NETMASK=$(grep "auto ${INTERFACE_NAME}" -A4 $INTERFACE_FILE | grep netmask| awk '{print $2}')
    INTERFACE_GATEWAY=$(grep "auto ${INTERFACE_NAME}" -A4 $INTERFACE_FILE | grep gateway| awk '{print $2}')

    DNS_1=$(awk 'NR==1 {print}' $DNS_FILE | awk '{print $2}')
    DNS_2=$(awk 'NR==2 {print}' $DNS_FILE | awk '{print $2}')

    INTERFACE_NETWORK=$(ipcalc $INTERFACE_ADDRESS/$INTERFACE_NETMASK | grep "Network" | cut -d' ' -f4)

    # ECHO
    # echo -e "${INTERFACE_ADDRESS}\n${INTERFACE_NETMASK}\n${INTERFACE_GATEWAY}\n${INTERFACE_NETWORK}\n${DNS_1}\n${DNS_2}"

    # FLUSH TABLE
    nft flush ruleset

    # ADD TABLE
    nft add table inet filter

    # ADD CHAIN (INPUT/OUTPUT) IN TABLE
    nft add chain inet filter input { type filter hook input priority 0\; }
    nft add chain inet filter output { type filter hook output priority 0\; }


    ## INPUT RULES
    # Allow SSH
    nft add rule inet filter input iif $INTERFACE_NAME ip saddr $INTERFACE_NETWORK ip daddr $INTERFACE_ADDRESS tcp dport 22 accept
    # Allow HTTP
    nft add rule inet filter input iif $INTERFACE_NAME ip saddr $INTERFACE_NETWORK ip daddr $INTERFACE_ADDRESS tcp dport 80 accept
    # Allow HTTPS
    nft add rule inet filter input iif $INTERFACE_NAME ip saddr $INTERFACE_NETWORK ip daddr $INTERFACE_ADDRESS tcp dport 443 accept
    # Allow DNS
    nft add rule inet filter input iif $INTERFACE_NAME ip saddr $DNS_1 ip daddr $INTERFACE_ADDRESS udp dport 53 accept
    if [ -n "$DNS_2" ]
    then
        nft add rule inet filter input iif $INTERFACE_NAME ip saddr $DNS_2 ip daddr $INTERFACE_ADDRESS udp dport 53 accept
    fi
    # Allow REDIS
    nft add rule inet filter input iif $INTERFACE_NAME ip saddr $INTERFACE_NETWORK ip daddr $INTERFACE_ADDRESS tcp dport 6380 accept
    # Allow PGADMIN
    nft add rule inet filter input iif $INTERFACE_NAME ip saddr $INTERFACE_NETWORK ip daddr $INTERFACE_ADDRESS tcp dport 8181 accept
    # Drop ALL
    nft add rule inet filter input iif $INTERFACE_NAME ip saddr 0.0.0.0/0 ip daddr $INTERFACE_ADDRESS drop


    ## OUTPUT RULES
    # Allow SSH
    nft add rule inet filter output oif $INTERFACE_NAME ip saddr $INTERFACE_ADDRESS tcp sport 22 ip daddr $INTERFACE_NETWORK accept
    # Allow HTTPS
    nft add rule inet filter output oif $INTERFACE_NAME ip saddr $INTERFACE_ADDRESS tcp sport 443 ip daddr 0.0.0.0/0 accept
    # Allow DNS
    nft add rule inet filter output oif $INTERFACE_NAME ip saddr $INTERFACE_ADDRESS ip daddr $DNS_1 udp dport 53 accept
    if [ -n "$DNS_2" ]
    then
        nft add rule inet filter output oif $INTERFACE_NAME ip saddr $INTERFACE_ADDRESS ip daddr $DNS_2 udp dport 53 accept
    fi
    # Allow REDIS
    nft add rule inet filter output oif $INTERFACE_NAME ip saddr $INTERFACE_ADDRESS tcp sport 6380 ip daddr 0.0.0.0/0 accept
    # Allow PGADMIN
    nft add rule inet filter output oif $INTERFACE_NAME ip saddr $INTERFACE_ADDRESS tcp sport 8181 ip daddr 0.0.0.0/0 accept
    # Drop ALL
    nft add rule inet filter output oif $INTERFACE_NAME ip saddr $INTERFACE_ADDRESS ip daddr 0.0.0.0/0 drop

    # SAVE POLICY
    nft list ruleset > /etc/nftables.conf

    # RESTART SERVICE NFTABLES
    systemctl restart nftables.service
fi
