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





"""
sql_table_creation_or_updation(dbname="Shopify",tablename="po_cod",replace_or_append="replace",
                               input_file_dir=dir_switch(win=win_shopify_cod,lin=lin_shopify_cod))
"""





from dotenv import load_dotenv
import requests
from amazon.order_table_updater import get_access_token
load_dotenv()

REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SP_API_DEFAULT_MARKETPLACE = os.getenv("SP_API_DEFAULT_MARKETPLACE")




def createReport():
    base_url = "https://sellingpartnerapi-eu.amazon.com/reports/2021-06-30/reports"
    endpoint = '/reports/2021-06-30/reports'
    headers = {
            "x-amz-access-token": get_access_token(),
            "Content-Type": "application/json"
            }
    data = {
        "reportType":"GET_MERCHANTS_LISTINGS_FYP_REPORT",
        "marketplaceIds" : ["A21TJRUUN4KGV"]
     }
    
    response = requests.post(base_url,headers=headers, json=data)
    status_message(message=f"Status code : {response.status_code}",color='blue')
    status_message(message="Response \n :",color='blue')
    response.raise_for_status()
    return response.json()


json_updater(field="latest_access_token_request",
                updated_value=str(datetime.now()),
                filepath=win_api_config)




"""
sql_table_creation_or_updation(dbname='Shopify',tablename="sh_orders",replace_or_append="append",
                               input_file_dir=win_shopify_order_excel_file
                            )
"""

h = r"D:\4.Phonepe"


























#json_updater(field="latest_access_token_request",updated_value=datetime.now().isoformat(),
#           filepath=dir_switch(win=win_api_config,lin=lin_api_config))