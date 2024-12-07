from helpers.sql_scripts import sql_table_CR
from helpers.file_ops import *
from sales.views import *
from amazon.sp_api_utilities import *

  

orders = sp_api_report_df(report_type="GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
                           start_date=from_timestamp(4),end_date=from_timestamp(0))

#filtered_df = df["order_status"] == "Pending - Waiting for Pick Up"


fields = ["amazon_order_id","purchase_date","last_updated_date","order_status","product_name","item_status","quantity","item_price","item_tax","shipping_price","shipping_tax"]
selected_fields = orders.filter(items=fields)

waiting_for_pickup = selected_fields.loc[orders['order_status'] == "Pending - Waiting for Pick Up"]

if waiting_for_pickup.empty() == True:
    color_text(message="No scheduled orders right now.")

# 50859020064

