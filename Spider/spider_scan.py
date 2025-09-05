import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from time import sleep
import random
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Class for allowing older SSL/TLS protocols
class TLSAdapter(HTTPAdapter):
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_context = create_urllib3_context(ssl_version=ssl_version)
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

visited_urls = set()
urls_with_forms = set()

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to fetch URLs with retries and SSL fixes
def fetch_url_with_retries(url, retries=3, verify_ssl=True):
    session = requests.Session()
    adapter = TLSAdapter()
    session.mount('https://', adapter)

    for attempt in range(retries):
        try:
            response = session.get(url, headers=headers, timeout=10, verify=verify_ssl)
            if response.status_code == 403:
                print("Blocked by server (403), retrying with delay...")
                sleep(random.uniform(1, 3))
            else:
                return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
    return None

# Function to spider a website
def spider(url, max_depth=2, depth=0):
    if depth > max_depth or url in visited_urls:
        return

    print(f"Visiting: {url}")
    visited_urls.add(url)

    try:
        response = fetch_url_with_retries(url, verify_ssl=True)
        if not response:
            print(f"Trying to fetch {url} without SSL verification...")
            response = fetch_url_with_retries(url, verify_ssl=False)

        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find forms and input fields
            if soup.find('form'):  # Check if any <form> tags exist on the page
                urls_with_forms.add(url)

            # Recursively follow links
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if is_valid_url(next_url, url):
                    spider(next_url, max_depth, depth + 1)

    except Exception as e:
        print(f"Error visiting {url}: {e}")

def is_valid_url(next_url, base_url):
    """
    Checks if a URL is valid and within the base domain.
    """
    parsed_next = urlparse(next_url)
    parsed_base = urlparse(base_url)
    return (parsed_next.netloc == parsed_base.netloc and
            parsed_next.scheme in ['http', 'https'])

def write_results_to_file(filename):
    """
    Writes the URLs with forms to a file.
    :param filename: The name of the file to write.
    """
    with open(filename, 'w') as file:
        for url in urls_with_forms:
            file.write(f"{url}\n")
    print(f"\nURLs with forms written to {filename}")

# Start spidering
start_url = input("Enter the URL to spider: ").strip()
output_file = "urls_with_input_fields.txt"

spider(start_url)
write_results_to_file(output_file)

