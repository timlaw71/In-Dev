import requests
from bs4 import BeautifulSoup
import argparse
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from openpyxl import Workbook

# Class for allowing older SSL/TLS protocols
class TLSAdapter(HTTPAdapter):
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_context = create_urllib3_context(ssl_version=ssl_version)
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

visited_urls = set()
urls_with_forms = {}
redirected_urls = []

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
            response = session.get(url, headers=headers, timeout=10, verify=verify_ssl, allow_redirects=False)
            if response.status_code in (301, 302):
                # Capture redirect information
                redirect_location = response.headers.get('Location', 'Unknown')
                redirected_urls.append((url, redirect_location))
                print(f"Redirect detected: {url} -> {redirect_location}")
                return None
            if response.status_code == 403:
                print(f"Blocked by server (403) at {url}, retrying...")
            else:
                return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
    return None

# Function to spider a website
def spider(url):
    """
    Visits a URL and checks for input fields without following links.
    """
    print(f"Visiting: {url}")
    visited_urls.add(url)

    try:
        response = fetch_url_with_retries(url, verify_ssl=True)
        if not response:
            return

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find forms and input fields
            forms = soup.find_all('form')
            if forms:
                input_types = set()
                for form in forms:
                    for input_field in form.find_all('input'):
                        input_type = input_field.get('type', 'text')  # Default to 'text' if type is not specified
                        input_types.add(input_type)

                # Store URL with input field types
                urls_with_forms[url] = list(input_types)

    except Exception as e:
        print(f"Error visiting {url}: {e}")

def write_results_to_excel(filename):
    """
    Writes the results to an Excel file with two sheets: "URLs with Forms" and "Redirected URLs".
    :param filename: The name of the Excel file to write.
    """
    workbook = Workbook()
    
    # Sheet 1: URLs with Forms
    forms_sheet = workbook.active
    forms_sheet.title = "URLs with Forms"
    forms_sheet.append(["URL", "Input Types"])
    for url, input_types in urls_with_forms.items():
        forms_sheet.append([url, ", ".join(input_types)])
    
    # Sheet 2: Redirected URLs
    redirects_sheet = workbook.create_sheet(title="Redirected URLs")
    redirects_sheet.append(["URL", "Redirect Location"])
    for url, redirect_location in redirected_urls:
        redirects_sheet.append([url, redirect_location])
    
    # Save the workbook
    workbook.save(filename)
    print(f"\nResults written to Excel file: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Spider URLs, extract those with input fields, and capture redirects.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input file containing URLs (one per line).")
    parser.add_argument("-o", "--output", required=True, help="Path to the Excel output file.")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    # Read URLs from the input file
    try:
        with open(input_file, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    # Spider each URL
    for url in urls:
        spider(url)

    # Write results to the Excel file
    write_results_to_excel(output_file)

if __name__ == "__main__":
    main()
