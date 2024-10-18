import requests
import json

# Replace with your SP API credentials and endpoint
endpoint = 'https://sellingpartnerapi-fe.amazon.com'
access_token = 'YOUR_ACCESS_TOKEN'  # Obtain via OAuth

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Make a request to get marketplace participations
response = requests.get(f'{endpoint}/markets', headers=headers)

if response.status_code == 200:
    marketplaces = response.json()
    for market in marketplaces['payload']['marketplaceParticipations']:
        if market['marketplaceId'] == 'A21TJRUUN4KGV':  # Marketplace ID for Amazon India
            print(f"Marketplace ID: {market['marketplaceId']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
