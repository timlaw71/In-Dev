import mmh3
import requests
import codecs
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import shodan

# Replace 'YOUR_SHODAN_API_KEY' with your actual Shodan API key
SHODAN_API_KEY = 'sKjbp25u11Co6tHEvLZelqD8yEhoNFS2'
api = shodan.Shodan(SHODAN_API_KEY)

# Suppress warnings about insecure HTTPS requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if len(sys.argv) < 2:
    print("[!] Error!")
    print(f"[-] Use: python3 {sys.argv[0]} http://example.com")
    sys.exit()

def find_favicon_url(base_url):
    # First try fetching favicon.ico directly
    for favicon_path in ['/favicon.ico', '/favicon.png']:
        favicon_url = urljoin(base_url, favicon_path)
        try:
            response = requests.get(favicon_url, verify=False)
            print(f"Trying {favicon_url}, Status Code: {response.status_code}")  # Debug print
            if response.status_code == 200:
                return favicon_url
        except Exception as e:
            print(f"Error attempting to fetch {favicon_url}: {e}")

    # If direct fetch fails, look in the HTML for the favicon link
    try:
        response = requests.get(base_url, verify=False)
        print(f"Fetching HTML, Status Code: {response.status_code}")  # Debug print
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            favicon_links = soup.find_all("link", rel=lambda value: value and value.lower() in ["icon", "shortcut icon", "apple-touch-icon"])
            for link in favicon_links:
                favicon_href = link.get("href")
                if favicon_href:
                    favicon_absolute_url = urljoin(base_url, favicon_href)
                    print(f"Favicon found in HTML: {favicon_absolute_url}")  # Debug print
                    return favicon_absolute_url
    except Exception as e:
        print(f"Error fetching the favicon URL from HTML: {e}")

    return None

    # First try fetching favicon.ico directly
    for favicon_path in ['/favicon.ico', '/favicon.png']:
        favicon_url = urljoin(base_url, favicon_path)
        try:
            response = requests.get(favicon_url, verify=False)
            if response.status_code == 200:
                return favicon_url
        except Exception as e:
            print(f"Error attempting to fetch {favicon_url}: {e}")

    # If direct fetch fails, look in the HTML for the favicon link
    try:
        response = requests.get(base_url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            favicon_links = soup.find_all("link", rel=lambda value: value and value.lower() in ["icon", "shortcut icon", "apple-touch-icon"])
            for link in favicon_links:
                favicon_href = link.get("href")
                if favicon_href:
                    # Ensure the favicon link is absolute
                    return urljoin(base_url, favicon_href)
    except Exception as e:
        print(f"Error fetching the favicon URL from HTML: {e}")

    return None

def search_shodan(hash_favicon):
    try:
        # Search Shodan for the favicon hash
        results = api.search(f"http.favicon.hash:{hash_favicon}")
        print(f"Shodan found {results['total']} results for the favicon hash.")
        for result in results['matches']:
            print(f"IP: {result['ip_str']} - Port: {result['port']} - Org: {result.get('org', 'n/a')}")
    except shodan.APIError as e:
        print(f"Error: {e}")

def main():
    base_url = sys.argv[1]
    favicon_url = find_favicon_url(base_url)
    if favicon_url:
        print(f"Favicon found at: {favicon_url}")  # Print the full favicon URL
        response = requests.get(favicon_url, verify=False)
        favicon = codecs.encode(response.content, "base64")
        hash_favicon = mmh3.hash(favicon)

        print("[!] http.favicon.hash:" + str(hash_favicon))

        # Search for the hash in Shodan
        search_shodan(hash_favicon)
    else:
        print("Could not find a favicon link in the HTML of the provided URL.")

if __name__ == '__main__':
    main()
