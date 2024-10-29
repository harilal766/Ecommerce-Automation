from helpers.pdf_pattern_finder import *
from helpers.sql_scripts import query_backup,line_limit_checker
from helpers.loading_animations import loading_animation
from helpers.regex_patterns import *
import pg8000
import pandas as pd
import os
"""
    make the query for filtering orders form sql table bsaed on seperate cod and non cod pdf files
"""
def shipment_report(pdf_path,pattern,fields,database,table,id,order_by_clause,sql_filename,out_excel_path):
    order_ids = None
    order_id_list = pdf_pattern_finder(filepath=pdf_path,pattern=pattern)
    #last_column = order_id_list[-1]
    try:
        order_ids = ""; order_id_count =0
        for order_id in order_id_list:
            order_id_count+=1
            if order_id_list[-1] == order_id:
                order_ids+= f"'{order_id}'"
            elif line_limit_checker(word_count=order_id_count,line_limit=3):
                order_ids+= f"'{order_id}',\n"
            elif not line_limit_checker(word_count=order_id_count,line_limit=3):
                order_ids+= f"'{order_id}',"

            
            # avoiding the comma from the last column
        # Strip comma from last order id by identifying it using the pattern
        shipment_report_query = f"""
            SELECT DISTINCT
            {fields} 
            FROM {table} 
            WHERE {id} IN (
                \t{order_ids}
            )
            ORDER BY {order_by_clause};
        """
        #loading_animation(len(order_ids)), ask for the loading value and execute the loading animation only while it is not executed. 

        conn = pg8000.connect(
            user='postgres',
            password='1234',
            host='localhost',      
            port=5432,            
            database='Amazon'
        )

        cursor = conn.cursor()
        cursor.execute(shipment_report_query)
        results = cursor.fetchall()
        # Print the results
        for row in results:
            pass
        # excel conversion
        column_list = [desc[0] for desc in cursor.description]
        excel_sheet = pd.DataFrame(results,columns=column_list)

        out_excel_file = input("Enter the name for excel file : ")
        excel_sheet.to_excel(os.path.join(out_excel_path,out_excel_file+".xlsx"),index=False,engine='openpyxl')

        # Backing up the query
        query_backup(f"{sql_filename}",shipment_report_query)
    except Exception as e:
        better_error_handling(e)
    finally:
        cursor.close()
        conn.close()
        print(shipment_report_query)
















# Driver code for report generator
def report_driver(report_type): 
    report_type = report_type.lower()
    if "amazon" in report_type:
        shipment_report(
            #pdf_path="/home/hari/Desktop/Automation/Test documents/amazon shipping label",
            pdf_path=r"D:\5.Amazon\Mathew global\INvoice",
            pattern=amazon_order_id_pattern,
            fields="""amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax""",
            database="Amazon",table="Orders", id = "amazon_order_id",
            order_by_clause="product_name asc,quantity asc",
            sql_filename="amzn_shipment_query",
            out_excel_path=r"D:\5.Amazon\Mathew global\Scheduled report"
        )
    elif "shopify" in report_type:
        shipment_report(
            #pdf_path="/home/hari/Desktop/Automation/Test documents/post shipping labes",
            pdf_path=r"D:\6.SPEED POST\1.Shipping labels",
            pattern=post_order_id_pattern,
            fields=""" Name, Financial_Status, Paid_at, Fulfillment_Status, Fulfilled_at, Subtotal, Shipping, Total, Lineitem_quantity, Lineitem_name,
                    Lineitem_price, Lineitem_compare_at_price, Shipping_Province_Name,""",
            database="Shopify",table="sh_orders",id="name",
            order_by_clause="lineitem_name ASC, lineitem_price ASC",
            sql_filename="post shipment report",
            out_excel_path=r"D:\3.Shopify\Date wise order list"
            
        )
