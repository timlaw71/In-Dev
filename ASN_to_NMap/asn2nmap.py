# fetch_prefixes.py
import requests
import sys

def fetch_prefixes(asn):
    url = f"https://api.bgpview.io/asn/{asn}/prefixes"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to retrieve prefixes for {asn}. HTTP Status: {response.status_code}")
        sys.exit(1)

    data = response.json()
    prefixes = [prefix['prefix'] for prefix in data['data']['ipv4_prefixes']]

    if prefixes:
        with open("asn_prefixes.txt", "w") as file:
            for prefix in prefixes:
                file.write(prefix + "\n")
        print(f"Prefixes written to asn_prefixes.txt")
    else:
        print(f"No prefixes found for {asn}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fetch_prefixes.py <ASN>")
        sys.exit(1)

    asn = sys.argv[1]
    fetch_prefixes(asn)

