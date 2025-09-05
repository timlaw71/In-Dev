import requests
import codecs

url = 'https://www.takeda.com/favicon.ico'
response = requests.get(url, verify=False)
favicon_base64 = codecs.encode(response.content, "base64").decode()
print(favicon_base64)

