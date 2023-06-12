#!/bin/bash

# Retrieve the IP address from the command-line argument
IP_ADDRESS=$1
SAVE_NAME=$2

# Run nmap on the provided IP address
nmap -p- -sC -oA $SAVE_NAME $IP_ADDRESS

# Exit the container
exit