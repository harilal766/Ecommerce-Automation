import requests
from datetime import datetime, timedelta, timezone
import json
import os
from dotenv import load_dotenv


created_after = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

load_dotenv()

# Replace these with your credentials
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

#SELLER_ID = "ACJLZEYR3QZJFCQ77FO2CO36MSZQ"
#DEVELOPER_ID = "-------"

#Oauth_authorization_URL = f"https://sellercentral.amazon.com/apps/authorize/consent?selling_partner_id={SELLER_ID}&developer_id={DEVELOPER_ID}&client_id={CLIENT_ID}"
#print(Oauth_authorization_URL)

# SP-API endpoint
ORDER_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com/orders/v0/orders"
#ORDER_ENDPOINT = "https://sandbox.sellingpartnerapi-eu.amazon.com/orders/v0/orders"

def get_access_token():
    """Obtain a new access token using the refresh token."""
    url = "https://api.amazon.com/auth/o2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json().get("access_token")

def get_order_data(access_token, created_after):
    """Fetch orders created after a specific date."""
    headers = {
        "x-amz-access-token": access_token,
        "Content-Type": "application/json",
    }
    params = {
        "MarketplaceIds": "A21TJRUUN4KGV",  # Use your Marketplace ID
        "CreatedAfter": created_after,
    }

    response = requests.get(ORDER_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def main():
    try:
        # Step 1: Get Access Token
        access_token = get_access_token()
        #access_token = ACCESS_TOKEN
        # Step 2: Specify the date to filter orders (e.g., orders from the past 7 days)
        created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()

        # Step 3: Get order data
        orders = get_order_data(access_token, created_after)
        data = json.dumps(orders,indent=4)
        print("Order Data:", data)

    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", err)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()



