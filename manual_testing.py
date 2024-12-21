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
"""
    Index(['amazon_order_id', 'purchase_date', 'last_updated_date', 'order_status',
        'product_name', 'item_status', 'quantity', 'item_price', 'item_tax',
        'shipping_price', 'shipping_tax'], dtype='object')

"""

excel = pd.read_excel(r"D:\5.Amazon\Mathew global\Scheduled report\Scheduled for 2024-12-20 - COD.xlsx",
                      sheet_name="Sheet 1")


columns = ["quantity","item_price",'item_tax','shipping_price', 'shipping_tax']

def shipment_report_pivot_table(df,grouping_column,pivot_columns):
    try:
        if not df.empty:
            pivot = pd.pivot_table(data=df,index=grouping_column,
                                values= pivot_columns,aggfunc="sum")
            """
                Select the column you want to group : Product name
                Selct the operation you want on the pivot table : sum
                select the 
            """
            pivot.to_excel(excel_writer="D:\Ecom-Dashboard\Test documents\pivot\pivot.xlsx")
            # index names sorting should be changed to descending order
            

            # SORTING the pivot table 
            pivot = pivot[pivot_columns] # column sorting

            # Creating the sum row and adding to the pivot

            sum_row = pivot.sum(axis=0).to_frame().T
            sum_row.index = ["Total"]
            pivot = pd.concat(objs=[pivot,sum_row])

            # Final out
            color_text(message=pivot)
            
        else:
            color_text(message="The excel file is empty",color="red")

    except Exception as e:
        better_error_handling(e)
    

shipment_report_pivot_table(df=excel,grouping_column="product_name",pivot_columns=columns)