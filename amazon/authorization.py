import requests
from datetime import datetime, timedelta, timezone
from helpers.messages import color_print
from helpers.file_ops import *
from dotenv import load_dotenv
import os



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
    
current_time = datetime.now()
data = json_handler(filepath=dir_switch(win=win_api_config,lin=lin_api_config),operation='read')
last_request_time = datetime.fromisoformat(data['latest_access_token_request'])
difference_seconds = (current_time - last_request_time).total_seconds()
limit = 3600

def generate_access_token():
    url = "https://api.amazon.com/auth/o2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            color='green'
        else:
            color='red'
        color_print(f"Response Status Code: {response.status_code}",color=color)

        #print(f"Response Content: {response.text}")  # Log server response
        response.raise_for_status()  # Raise error if response status isn't 200
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Access Token Error: {e}")
        return None

def is_access_token_expired():
    if difference_seconds < limit:
        return False
    else:
        return True
    




def get_or_generate_access_token():
    try:
        pass
        # if the access token is expired
            # if yes, generate a new one.
                # Store the new one in to the json file
        # else
            # extract the access token from the env file and return it
    except Exception as e:
        better_error_handling(e)
        


