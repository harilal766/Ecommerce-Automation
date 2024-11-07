import requests
from datetime import datetime, timedelta, timezone
import json
import os,sys



created_after = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
from dotenv import load_dotenv




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
BASE_URL = "https://sellingpartnerapi-eu.amazon.com/"
ORDER_ENDPOINT = "orders/v0/orders"
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



class SPAPIBase:
    def __init__(self,access_token=get_access_token(),base_url="https://sellingpartnerapi-eu.amazon.com/",marketplace_id="A21TJRUUN4KGV"):
        self.access_token=access_token
        self.base_url=base_url
        self.marketplace_id=marketplace_id

class Orders:
    def getOrders(created_after,order_status):
        """ 
        Order api function parameters (optional)
        link : https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#getorders

        getOrders, getOrder
getOrderBuyerInfo
        getOrderAddress
        getOrderItems
        getOrderItemsBuyerInfo
        updateShipmentStatus
        getOrderRegulatedInfo
        updateVerificationStatus
        confirmShipment
    """
        access_token = get_access_token()
        headers = {
            "x-amz-access-token": access_token,
            "Content-Type": "application/json",
        }
        params = {
            "MarketplaceIds": "A21TJRUUN4KGV",  # Use your Marketplace ID
            "CreatedAfter": created_after,
            "OrderStatuses":order_status,
        }
        response = requests.get(BASE_URL+ORDER_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    

def driver():
    try:
        # Step 1: Get Access Token
        access_token = get_access_token()
        # Step 2: Specify the date to filter orders (e.g., orders from the past 7 days)
        created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()
            # CHOICES : PendingAvailability, Pending, PartiallyShipped, Shipped, InvoiceUnconfirmed 
        # Step 3: Get order data
        orders = Orders.getOrders(created_after,order_status="Unshipped")
        data = json.dumps(orders,indent=4)
        #print(data)
        print(f"First key : {next(iter(orders))}")
        print(orders)


    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", err)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    driver()



