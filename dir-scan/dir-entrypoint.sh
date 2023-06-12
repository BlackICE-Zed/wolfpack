#!/bin/sh

# Retrieve the target URL from the command-line argument
TARGET_URL=$1
WORDLIST=$2

# Run wfuzz on the provided target URL
wfuzz -c -z file,$WORDLIST --hh 0 --hc 404 $TARGET_URL > /app/dirscan.txt

# Exit the container
exit