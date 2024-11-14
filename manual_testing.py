from helpers.regex_patterns import *
from helpers.excel_to_sql_scripts import *
from helpers.sql_scripts import *
from helpers.file_ops import *
from helpers.messages import *
from report_generator import *

import sqlite3
import pandas as pd
import os

"""
    Filepath should be like this r"<path>"
"""
print("Code Testing")



"""
sql_table_creation_or_updation(dbname="Shopify",tablename="po_cod",replace_or_append="replace",
                               input_file_dir=dir_switch(win=win_shopify_cod,lin=lin_shopify_cod))
"""

"""
sql_table_creation_or_updation(dbname='Shopify',tablename="sh_orders",
                            replace_or_append="append",
                            input_file_dir=win_shopify_order_excel_file
                            )
"""




from dotenv import load_dotenv
import requests
from amazon.order_table_updater import get_access_token
from amazon.order_table_updater import Reports,Orders
from datetime import datetime, timedelta, timezone
load_dotenv()

REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SP_API_DEFAULT_MARKETPLACE = os.getenv("SP_API_DEFAULT_MARKETPLACE")



from bs4 import BeautifulSoup


article_no = "EL609980010IN"
post_track = f"https://api.cept.gov.in/CustomTracking/TrackConsignment.asmx/ArticleTracking?Article={article_no}&requestingApplication=Cust0M$Tr%40ck"

response = requests.get(post_track)
import xml.etree.ElementTree as ET

# Parse the XML content
root = ET.fromstring(response.content)

# Access specific data
for item in root.findall('.//YourElement'):
    print(item.text)











#json_updater(field="latest_access_token_request",updated_value=datetime.now().isoformat(),
#           filepath=dir_switch(win=win_api_config,lin=lin_api_config))

