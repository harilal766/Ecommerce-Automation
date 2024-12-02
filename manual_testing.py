from helpers.sql_scripts import sql_table_CR
from helpers.file_ops import *
from sales.views import *


"""
sql_table_CR(dbname="shopify",tablename="Orders",replace_or_append='replace',
             input_file_dir=win_shopify_fulfilled,filename="april.csv")
             """





"""
orders_instance = Orders()
orders = orders_instance.getOrders(CreatedAfter=iso_8601_timestamp(4),LatestShipDate=amzn_next_ship_date())
print(orders)
"""

