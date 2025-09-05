import re
import sys
from urllib.parse import urlparse


def parse_file(file_path):
    urls = set()  # Use a set to store unique URLs
    ips = set()   # Use a set to store unique IPs

    # Open and read the file
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace

            # Check if the line contains a URL
            if re.match(r'https?://', line):
                parsed_url = urlparse(line)
                # Construct the base URL (protocol + hostname)
                if parsed_url.scheme and parsed_url.hostname:
                    base_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
                    urls.add(base_url)

            # Check if the line contains an IP
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', line):
                ips.add(line)

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
        print(f"Unique IPs saved to 'unique_ips.txt'")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

