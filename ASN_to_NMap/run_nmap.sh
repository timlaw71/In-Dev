#!/bin/bash

# run_parallel_nmap.sh
if [ ! -f divided_prefixes.txt ]; then
    echo "Error: divided_prefixes.txt not found. Run the Python script to generate it."
    exit 1
fi

# Define the Nmap function to run for each subnet
nmap_scan() {
    prefix="$1"
    echo "Running Nmap scan on $prefix"
    nmap -Pn -sV -T4 -p 1-1000 "$prefix" -oN "nmap_result_${prefix//\//_}.txt"
}

export -f nmap_scan

# Use GNU Parallel to run the Nmap scans concurrently
cat divided_prefixes.txt | parallel -j 4 nmap_scan

