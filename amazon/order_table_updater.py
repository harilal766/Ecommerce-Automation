import requests
from datetime import datetime, timedelta, timezone
import json
import os,sys
from helpers.messages import status_message



created_after = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
from dotenv import load_dotenv




load_dotenv()

# Replace these with your credentials
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

#SELLER_ID = "ACJLZEYR3QZJFCQ77FO2CO36MSZQ"
#DEVELOPER_ID = "-------"

#Oauth_authorization_URL = f"https://sellercentral.amazon.com/apps/authorize/consent?selling_partner_id={SELLER_ID}&developer_id={DEVELOPER_ID}&client_id={CLIENT_ID}"
#print(Oauth_authorization_URL)

#ORDER_ENDPOINT = "https://sandbox.sellingpartnerapi-eu.amazon.com/orders/v0/orders"

def region_finder():
    pass

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
    try:
        # find the time in which last request was made and store it in a json file
        # if the date is same and the difference is  >= 1hr with current time,
            # request again.

        # if the list is empty add a number to avoid errors, this will make its legth 1.
        current_time = datetime.now()
        diference_seconds = ''
        status_message(message=f"last req : -------- , current time : {current_time}, difference : ",color='blue')
        response = requests.post(url, headers=headers, data=data)
        last_request_time = datetime.now()
        response.raise_for_status()
        access_token = response.json().get("access_token")
        if response.status_code == 200:
            status_message(message=f"Access Token Successfull.",color='green')
        else:
            status_message(message=f"Access code {response.status_code}",color='red')
        return access_token
    
    except requests.exceptions.RequestException as e:
        print(f"Access Token Error : {e}")
        return None



class SPAPIBase:
    def __init__(self,base_url="https://sellingpartnerapi-eu.amazon.com",marketplace_id="A21TJRUUN4KGV"):
        self.access_token = get_access_token()
        self.base_url = base_url
        self.marketplace_id = marketplace_id
        self.headers = {
            "x-amz-access-token": self.access_token,
            "Content-Type": "application/json"
            }
        # Common parameters, individual ones will be added from the respective functions
        self.params = {
            "MarketplaceIds": self.marketplace_id,
        }

class Orders(SPAPIBase):
    """ 
        Order api function parameters (optional)
        link : https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#getorders

        getOrders, getOrder, getOrderBuyerInfo, getOrderAddress, getOrderItems
        getOrderItemsBuyerInfo, updateShipmentStatus, getOrderRegulatedInfo
        updateVerificationStatus, confirmShipment
    """
    def getOrders(self,created_after,order_status):
        self.params.update({
            "CreatedAfter": created_after,
            "OrderStatuses":order_status,
        })
        endpoint = "/orders/v0/orders" 
        
        response = requests.get(self.base_url+endpoint, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()

    def getOrder(self,orderId):
        """
        Rate (requests per second)	Burst
                            0.5	    30
        """
        endpoint = f"/orders/v0/orders/{orderId}"
        self.params.update ({
            "orderId" : orderId
        })
        response = requests.get(self.base_url+endpoint, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()
    
    def getOrderBuyerInfo(self,orderId):
        """
        Rate (requests per second)	Burst
                            0.5	    30
        """
        endpoint = f"/orders/v0/orders/{orderId}/buyerInfo"
        self.params.update ({
            "orderId" : orderId
        })
        response = requests.get(self.base_url+endpoint, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()

    

class Reports():
    """
        https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-reference

        getReports, createReport, getReport, cancelReport
        getReportSchedules, createReportSchedule, getReportSchedule, cancelReportSchedule, getReportDocument
    """
    # Add getReports() here

    
    def createReport():
        base_url = "https://sellingpartnerapi-eu.amazon.com"
        endpoint = '/reports/2021-06-30/reports'
        headers = {
                "x-amz-access-token": f"bearer <{get_access_token()}>",
                "Content-Type": "application/json"
                }
        data = {
            "reportType":"GET_MERCHANTS_LISTINGS_FYP_REPORT",
            "marketplaceIds" : ["A21TJRUUN4KGV"]
        }
        
        response = requests.post(base_url+endpoint,headers=headers, json=data)
        status_message(message=f"Status code : {response.status_code}",color='blue')
        status_message(message="Response \n :",color='blue')
        #response.raise_for_status()
        return response.json()
    




