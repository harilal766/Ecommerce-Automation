from helpers.regex_patterns import *
from helpers.excel_to_sql_scripts import *
from helpers.sql_scripts import *
from helpers.file_ops import *
from helpers.messages import *
import sqlite3

from report_generator import *

import pandas as pd
import os
#pdf_pattern_finder(filepath=dir_switch(directory='post_label'),pattern=amazon_order_id_pattern)

"""
    Filepath should be like this r"<path>"
"""
print("Code Testing")

"""
create_table(sql_table_name="Transactions",
             file_path=r"D:\Ecommerce-Automation\Test documents\amazon settlement\Transaction table cod & prepaid.xlsx")
"""

#pdf_pattern_finder(filepath=r"D:\5.Amazon\Mathew global\INvoice",pattern=amazon_order_id_pattern) 

#report_driver("Amazon")



#print(sql_column_creator(filepath=r"D:\Ecommerce-Automation\Test documents\post orders sheet",filename="1.10.24.xlsx"))


#sql_columns_constructor(filepath=r"D:\Ecommerce-Automation\Test documents\post orders sheet\1.10.24.xlsx")
"""
data_import(tablename="Orders",
            sample_filepath=r"D:\Ecommerce-Automation\Test documents\post orders sheet\1.10.24.xlsx",
            input_filepath=r"D:\5.Amazon\Mathew global\Scheduled report")

"""

"""
data_import(tablename="Orders",
    sample_filepath=r"D:\5.Amazon\Mathew global\Scheduled report\order sample table.xlsx",
    input_filepath=r"D:\5.Amazon\Mathew global\Scheduled report",input_filename="1-31.txt")

"""

#shopify_order_excel_sample = r"D:\Ecommerce-Automation\Test documents\post orders sheet\1.10.24.xlsx"

#shopify_order_excel_sample = r"/home/hari/Desktop/Ecommerce-Automation/Test documents/post orders sheet/1.10.24.xlsx"
"""
list = sql_columns_constructor(filepath=shopify_order_excel_sample)

for i in list:
    print(f"{i} - {datatype_finder(i)}")
"""











#sql_table_creation_or_updation(dbname="Shopify",tablename="cod_oorja",replace_or_append="replace",input_file_dir=dir_switch(win=win_shopify_cod,lin=lin_shopify_cod))


from dotenv import load_dotenv
import requests
from amazon.order_table_updater import get_access_token
load_dotenv()

REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SP_API_DEFAULT_MARKETPLACE = os.getenv("SP_API_DEFAULT_MARKETPLACE")

credentials = dict(
    refresh_token=REFRESH_TOKEN,
    lwa_app_id=CLIENT_ID,
    lwa_client_secret = CLIENT_SECRET
)

base_url = "https://sellingpartnerapi-eu.amazon.com"
def getReport():
    endpoint = "/reports/2021-06-30/reports"
    headers = { 
        "x-amz-access-token": get_access_token(),
        "Content-Type": "application/json"
    }
    params = {
        "reportTypes" : "GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_SHIPPING",
    }

    response = requests.get(base_url+endpoint, headers=headers, params=params)
    status_message(message=f"Endpoint : {base_url+endpoint}",color='blue')
    status_message(message=response.text,color='blue')
    response.raise_for_status()
    return response.json()




"""------------------------"""
import requests
import time
from datetime import datetime
from requests.auth import AWS4Auth  # Needed for signing requests if IAM role is used
import boto3  # Only if using IAM roles

# Parameters to Update
access_token = "YOUR_ACCESS_TOKEN"  # Obtain this by refreshing your SP API token
client_id = "YOUR_CLIENT_ID"        # From Amazon Developer Console
client_secret = "YOUR_CLIENT_SECRET"
region = "eu-west-1"                # Replace with your region
endpoint = "https://sellingpartnerapi-eu.amazon.com"

# Optional IAM settings, needed only if your Report API requires it
aws_access_key = "YOUR_AWS_ACCESS_KEY"
aws_secret_key = "YOUR_AWS_SECRET_KEY"
session_token = None                # Only needed if using temporary credentials

# Set up endpoint and headers
report_type = "GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_SHIPPING"  # Example report type
url = f"{endpoint}/reports/2021-06-30/reports"
headers = {
    "x-amz-access-token": access_token,
    "Content-Type": "application/json",
    "User-Agent": "YourAppName/1.0 (Language=Python)"
}

# If IAM Authorization is Required
if aws_access_key and aws_secret_key:
    session = boto3.Session(aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_key,
                            region_name=region)
    credentials = session.get_credentials()
    auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'execute-api', session_token=session_token)
else:
    auth = None

# JSON Payload for Report Request
payload = {
    "reportType": report_type,
    "marketplaceIds": ["A21TJRUUN4KGV"],  # Update with your marketplace ID
}

# Making the Request
try:
    response = requests.post(url, headers=headers, json=payload, auth=auth)
    response.raise_for_status()  # Raise error for HTTP 4xx/5xx codes

    # Check Response
    if response.status_code == 202:
        report_data = response.json()
        report_id = report_data.get("reportId")
        print(f"Report requested successfully, report ID: {report_id}")
    else:
        print(f"Unexpected response: {response.status_code}, {response.text}")

except requests.exceptions.HTTPError as e:
    print(f"HTTPError: {e}")
except Exception as ex:
    print(f"An error occurred: {ex}")
