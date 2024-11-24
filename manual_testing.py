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



def filter_query_execution(dbname,db_system,tablename,filter_rows):
    try:
        
        fields = """amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax"""
        out_excel_path=dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)

        order_by_clause="product_name asc,quantity asc"
        query = f"""SELECT {fields}
          FROM {tablename} 
          where amazon_order_id in {tuple(filter_rows)}
          ORDER BY {order_by_clause};"""
        print(query)
        # connecting to the db
        connection = db_connection(dbname=dbname,db_system=db_system)
        if connection:
            success_status_msg("Connection Succeeded.")
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            # converting the sql result into excel file
            sql_to_excel(sql_cursor=cursor,query_result=results,out_excel_path=out_excel_path)

# Error Areas -----------------------------------------------------------------------------------
        else:
            color_text(message="Connection Failed",color="red")
    except Exception as e:
        better_error_handling(e)

    finally:
        success_status_msg(query)
        # closing the db
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and connection:
            connection.close()
        color_text(message="Connection closed.",color='green')
