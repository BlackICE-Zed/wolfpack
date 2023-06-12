#!/bin/sh

# Retrieve the target URL from the command-line argument
TARGET_URL=$1
WORDLIST=$2

# Run ffuf on the provided target URL and save the output to a file
ffuf -w $WORDLIST -u $TARGET_URL -fc 404 -o /app/dnsscan.txt

# Exit the container
exit