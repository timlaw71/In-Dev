import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4

url = "https://www.foxnews.com/"

# It's good practice to send a User-Agent header to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Fox News headlines are often in <h2> or <h3> tags with class="title"
# and the text is within an <a> tag inside them.
# We'll collect potential headline elements first.
# Using a set to store headline texts to avoid duplicates automatically.
headline_texts = set()

# Find all <h2> and <h3> tags with class 'title'
# These are common containers for headlines on Fox News.
# Note: Website structures can change! This selector might need updates in the future.
headline_containers = soup.find_all(["h2", "h3"], class_="title")

for container in headline_containers:
    # The actual headline text is usually within an <a> tag inside the container
    link_tag = container.find("a")
    if link_tag and link_tag.text:
        text = link_tag.text.strip()
        if text: # Ensure text is not empty after stripping
            headline_texts.add(text)
    # Fallback: sometimes the text might be directly in the h2/h3 if no <a>
    # (less common for clickable headlines but good to consider)
    elif container.text:
        text = container.text.strip()
        if text:
            headline_texts.add(text)


# Convert the set to a list to print them in some order (order from set is not guaranteed)
# and to take a slice.
final_headlines = list(headline_texts)

if not final_headlines:
    print("No headlines found. The website structure might have changed, or the selectors need adjustment.")
else:
    print(f"--- Top {min(10, len(final_headlines))} Headlines from Fox News ---")
    for i, headline_text in enumerate(final_headlines[:10], start=1):
        print(f"{i}. {headline_text}")

    print("\nNews fetched successfully!")
