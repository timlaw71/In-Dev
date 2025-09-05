import json
import datetime

# read in JSON file
with open('test_data.json', 'r') as f:
    data = json.load(f)

# get current date
today = datetime.datetime.now().date()

unique_domains = set()

for domain in data['search_result']:
    expiry_date = domain.get('expiry_date')
    if expiry_date is not None:
        expiry_date = datetime.datetime.strptime(expiry_date, '%Y-%m-%d').date()
        if expiry_date >= today:
            if domain['domain_name'] not in unique_domains:
                unique_domains.add(domain['domain_name'])
                print(domain['domain_name'])