import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4

url = "https://news.ycombinator.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

headlines = soup.find_all("span", class_="titleline")

for i, headline in enumerate(headlines[:10], start=1):
    print(f"{i}. {headline.find().text}")

print("News fetched successfully!")
