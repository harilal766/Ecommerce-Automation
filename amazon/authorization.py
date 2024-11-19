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
SP_API_DEFAULT_MARKETPLACE = os.getenv("SP_API_DEFAULT_MARKETPLACE")

#SELLER_ID = "ACJLZEYR3QZJFCQ77FO2CO36MSZQ"
#DEVELOPER_ID = "-------"

#Oauth_authorization_URL = f"https://sellercentral.amazon.com/apps/authorize/consent?selling_partner_id={SELLER_ID}&developer_id={DEVELOPER_ID}&client_id={CLIENT_ID}"
#print(Oauth_authorization_URL)

#ORDER_ENDPOINT = "https://sandbox.sellingpartnerapi-eu.amazon.com/orders/v0/orders"

def region_finder():
    pass
    
current_time = datetime.now()



def is_file_empty(filepath):
    data = dotenv_values(filepath)
    if len(data) == 0:
        color_print(message="This file is empty, please check",color='red')
        return True
    



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
        access_token = response.json().get("access_token")
    
        
        # Store the new token in to the env file before returning it.
        file_handler(filepath='.env',operation='update',
            field='ACCESS_TOKEN',updated_value=access_token)
        color_print(message="access token -> env file",color='green')
            # request time -> json file
        filepath = dir_switch(win=win_api_config,lin=lin_api_config)
        field = "latest_access_token_request"
        file_handler(filepath=filepath,field=field,
                    operation='update',updated_value=current_time)
        color_print(message="access token time -> json file",color='green')
        
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Access Token Error: {e}")
        return None






def get_or_generate_access_token():
    current_time = datetime.now()
    try:
        # initialization
        # Read the json file to get the time stamp
        data = file_handler(filepath=dir_switch(win=win_api_config,lin=lin_api_config),operation='read')
        
        
        last_request_time_str = data["latest_access_token_request"]
        last_request_time = datetime.fromisoformat(last_request_time_str)
        print(type(last_request_time))
        difference_seconds = (current_time - last_request_time).total_seconds()
        limit = 3600
        token_status = ''
        color_print(message=f"Last request : {last_request_time}, Current time : {current_time}, Difference : {difference_seconds} seconds.",color='blue')
        # if the access token is expired or access token field is empty.
        remaining_access_token = os.getenv("ACCESS_TOKEN")
            
        if (not last_request_time == "" ) and (difference_seconds > limit):
            color_print(message="Generating new token.",color='green')
            # generate a new one.
            new_access_token = generate_access_token()
            color_print(message=new_access_token,color='blue')

            """
            # Store the new token in to the env file
            file_handler(filepath='.env',operation='update',
                field='ACCESS_TOKEN',updated_value=new_access_token)
            # request time -> json file
            filepath = dir_switch(win=win_api_config,lin=lin_api_config)
            field = "latest_access_token_request"
            file_handler(filepath=filepath,field=field,
                        operation='update',updated_value=current_time)
            """

            return new_access_token
        elif (difference_seconds < limit):
            color_print(message="Previous Token can be used.",color='green')
            # extract the access token value from the env file and return it
            previous_access_token = os.getenv('ACCESS_TOKEN')
            # Status message for old token
           
            return previous_access_token
            
    except AttributeError:
        remaining_access_token = ''
    except Exception as e:
        better_error_handling(e)
    
        
        


def rate_limit_checker(response):
    print(response.headers)