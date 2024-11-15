from helpers.regex_patterns import *
from helpers.excel_to_sql_scripts import *
from helpers.sql_scripts import *
from helpers.file_ops import *
from helpers.messages import *
from report_generator import *

import sqlite3
import pandas as pd
import os











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





#json_updater(field="latest_access_token_request",updated_value=datetime.now().isoformat(),
#           filepath=dir_switch(win=win_api_config,lin=lin_api_config))


# API TESTING
"""
created_after = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
instance = Orders()
response = instance.getOrders(CreatedAfter=created_after,OrderStatuses='Unshipped')
"""

today_string = str(datetime.today()).split(" ")[0]
#print(today_string)





#sql_table_creation_or_updation(dbname="Amazon",tablename="Returns",replace_or_append='append',input_file_dir=win_amazon_return)


