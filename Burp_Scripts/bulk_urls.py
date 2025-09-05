import requests

# Burp Proxy Configuration
proxies = {
    "http": "http://127.0.0.1:8080",  # Replace with your Burp proxy address
    "https": "http://127.0.0.1:8080"
}

# Function to add http:// or https:// if missing
def add_scheme(url, scheme="http"):
    if not url.startswith(("http://", "https://")):
        return f"{scheme}://{url}"
    return url

# Read the list of URLs
with open("urls.txt", "r") as file:
    urls = file.readlines()

# Send each URL through Burp
for url in urls:
    url = url.strip()  # Remove leading/trailing whitespace
    url_http = add_scheme(url, "http")  # Try http first
    url_https = add_scheme(url, "https")  # Use https as fallback
    
    try:
        response = requests.get(url_http, proxies=proxies, verify=False)
        print(f"Visited {url_http} - Status Code: {response.status_code}")
    except Exception as e_http:
        print(f"Error visiting {url_http}: {e_http}")
        try:
            response = requests.get(url_https, proxies=proxies, verify=False)
            print(f"Visited {url_https} - Status Code: {response.status_code}")
        except Exception as e_https:
            print(f"Error visiting {url_https}: {e_https}")

