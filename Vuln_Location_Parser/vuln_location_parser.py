import re
import sys
from urllib.parse import urlparse


def parse_file(file_path):
    urls = set()  # Use a set to store unique URLs
    ips = set()   # Use a set to store unique IPs

    # Open and read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Extract and clean up the URL
            url_match = re.search(r'URL:\s*(https?://[^\s]+)', line)
            if url_match:
                full_url = url_match.group(1).strip()
                parsed_url = urlparse(full_url)
                # Construct the base URL (protocol + hostname)
                if parsed_url.scheme and parsed_url.hostname:
                    base_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
                    urls.add(base_url)  # Add to set to ensure uniqueness

            # Extract data to the right of 'IP:' and keep the port, remove '(TCP)' and quotes
            ip_match = re.search(r'IP:\s*([\d\.]+:\d+)', line)
            if ip_match:
                ip = ip_match.group(1).strip()  # Extract IP with port
                ips.add(ip)  # Add to set to ensure uniqueness

    return sorted(urls), sorted(ips)  # Sort for consistent output


def save_to_file(data, file_name):
    with open(file_name, 'w') as file:
        for item in data:
            file.write(item + '\n')


def main():
    # Check if the file path was provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    # Get the file path from the command-line argument
    file_path = sys.argv[1]

    try:
        # Parse the file
        urls, ips = parse_file(file_path)

        # Save results to files
        save_to_file(urls, "unique_urls.txt")
        save_to_file(ips, "unique_ips.txt")

        # Print the results
        print(f"Unique base URLs saved to 'unique_urls.txt'")
        print(f"Unique IPs with ports saved to 'unique_ips.txt'")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

