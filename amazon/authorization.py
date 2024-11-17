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
    
def is_access_token_expired():
    # if the difference is more than limit, return false , if within limit, return True
    current_time = datetime.now()
    # find the time in which last request was made and store it in a json file
        # if the date is same and the difference is  >= 1hr with current time,
            # request again.
        # if the list is empty add a number to avoid errors, this will make its legth 1.
    data = json_reader(dir_switch(win=win_api_config,lin=lin_api_config))
    last_request_time = datetime.fromisoformat(data['latest_access_token_request'])
    difference_seconds = (current_time - last_request_time).total_seconds()
    limit = 3600
    color_print(message=f"last request at : {last_request_time}, current time : {current_time}, difference : {difference_seconds} seconds.",color='blue')
    
    
    if difference_seconds < limit:
        return False
    else:
        color_print(message=f"access token expired, requesting again...",color='blue')
        # Storing the new access token to the .env file.
        request_time = datetime.now().isoformat()

        # Update the request time to a json file for later use...
        json_updater(field="latest_access_token_request",updated_value=request_time,
                                filepath=dir_switch(win=win_api_config,lin=lin_api_config))
        access_token_storing = env_file_updater(key='ACCESS_TOKEN',current_value=os.getenv('ACCESS_TOKEN'),new_value=access_token)
        if access_token_storing:
            color_print(message="Access token stored to the env file.",color='green')
        else:
            color_print(message="Access token didn't stored to the env file.",color='red')
        return True
    
    
    
    
            
    

def get_access_token():
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
