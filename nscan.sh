#!/bin/bash

# Check if an argument was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <subnet>"
    echo "Example: $0 192.168.1.0/24"
    exit 1
fi

# Set the subnet from the first argument
subnet=$1

echo "Scanning network $subnet for active hosts..."
echo "IP Address       Hostname"

# Function to ping and resolve hostname
ping_and_resolve() {
    full_ip="$subnet_prefix.$1"
    # Ping the IP address
    ping -c 1 $full_ip &> /dev/null
    if [ $? -eq 0 ]; then
        # If the ping is successful, try to get the hostname
        hostname=$(nslookup $full_ip 2>/dev/null | awk '/name =/ {print $4}' | sed 's/.$//')
        # If nslookup does not return a hostname, set it as Unknown
        if [ -z "$hostname" ]; then
            hostname="Unknown"
        fi
        # Output the IP address and hostname
        echo -e "$full_ip\t$hostname"
    fi
}

export -f ping_and_resolve

# Remove the CIDR notation to extract the subnet prefix
subnet_prefix=$(echo $subnet | cut -d'/' -f1)
last_octet=$(echo $subnet_prefix | cut -d'.' -f4)
start=1
end=254
# Adjust the start and end if the subnet prefix ends in 0, indicating a full range
if [ "$last_octet" -eq "0" ]; then
    subnet_prefix=$(echo $subnet_prefix | sed 's/.0$//')
else
    start=$(($last_octet + 1))
    end=$start
fi

export subnet_prefix

# Use xargs to run the function in parallel
seq $start $end | xargs -n 1 -P 20 -I {} bash -c 'ping_and_resolve "$@"' _ {}

echo "Scan complete."
