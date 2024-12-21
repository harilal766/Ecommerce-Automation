from helpers.sql_scripts import sql_table_CR
from helpers.messages import *
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *


# time is must, if days == 0 , treat time as of todays
# for normal timestamp, there shouldnt be much parameters
# if date is needed only and not time type is not needed.
def timestamp(days,type=None,split=None):
    # types : iso 8601, 
    ind_timestamp = (datetime.now(timezone("Asia/Kolkata"))-timedelta(days=days))
    if type == "iso":
        return ind_timestamp.isoformat()
    elif type == "utc":
        return ind_timestamp.utcnow()
    # if the split is none, return the full time stamp




import pandas as pd

excel = pd.read_excel(r"D:\5.Amazon\Mathew global\Scheduled report\Scheduled for 2024-12-20 - COD.xlsx",
                      sheet_name="Sheet 1")

columns = ["quantity","item_price",'item_tax','shipping_price', 'shipping_tax']

def shipment_report_pivot_table(df,grouping_column,columns):
    try:
        """
        Index(['amazon_order_id', 'purchase_date', 'last_updated_date', 'order_status',
            'product_name', 'item_status', 'quantity', 'item_price', 'item_tax',
            'shipping_price', 'shipping_tax'],
            dtype='object')

        """
        pivot = pd.pivot_table(data=excel,index=grouping_column,
                            values= columns,aggfunc="sum"
            )
        """
            Select the column you want to group : Product name
            Selct the operation you want on the pivot table : sum
            select the 
        """
        pivot.to_excel(excel_writer="D:\Ecom-Dashboard\Test documents\pivot\pivot.xlsx")
        # index names sorting should be changed to descending order
        sum_row_list = ["None"]

        for column in columns:
            sum_row_list.append(sum(pivot[column]))

        print(pivot)
        print(sum_row_list)
    except Exception as e:
        better_error_handling(e)
    

shipment_report_pivot_table(df=excel,grouping_column="product_name",columns=columns)