from amazon.response_manipulator import n_days_timestamp,sp_api_report_df_generator
from helpers.file_ops import *
from amazon.report_types import *


file_dir = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
filename=f"16 - 23.csv"


from helpers.sql_scripts import db_connection,sql_table_CR
from report_generator import *
from amazon.api_models import *
from amazon.response_manipulator import *
import pandas as pd

"""
# converting the data to sql for querying
df = sp_api_report_df_generator(report_type=order_report_types["datewise orders data flatfile"],
                        start_date=n_days_timestamp(7),end_date=n_days_timestamp(0))

print(df)


df.to_sql(name="Test",con=db_connection(dbname="Amazon",db_system='sqlite'),if_exists= 'replace',index=False)

"""
# querying the sql table and finding cod and prepaid reports seperately
ord_ins = Orders(); created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()
ord_resp = ord_ins.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")

orders = sp_api_shipment_summary(response=ord_resp)

cod_order_ids = orders.cod; prepaid_order_ids = orders.prepaid

print(cod_order_ids)
print(prepaid_order_ids)


