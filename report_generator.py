from helpers.pdf_pattern_finder import *
from helpers.sql_scripts import psql_connector,query_backup,line_limit_checker
from helpers.loading_animations import loading_animation
from helpers.regex_patterns import *


"""
    make the query for filtering orders form sql table bsaed on seperate cod and non cod pdf files
"""
        

def shipment_report(pdf_path,pattern,fields,table,id,order_by_clause,sql_filename):
    out_excel_path = None
    order_ids = None
    order_id_list = pdf_pattern_finder(filepath=pdf_path,pattern=pattern)
    #last_column = order_id_list[-1]
    try:
        order_ids = ""; order_id_count =0
        for order_id in order_id_list:
            order_id_count+=1
            if line_limit_checker(word_count=order_id_count,line_limit=3):
                order_ids+= f"'{order_id}',\n"
            else:
                order_ids+= f"'{order_id}',"
            # avoiding the comma from the last column
        shipment_report_query = f"""
            SELECT DISTINCT
            {fields} 
            FROM {table} 
            WHERE {id} IN (
                \t{order_ids}
            )
            ORDER BY {order_by_clause};
        """
        #loading_animation(len(order_ids))
        # Backing up the query
        query_backup(f"{sql_filename}",shipment_report_query)
    except Exception as e:
        better_error_handling(e)
    finally:
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
            table="Orders", id = "amazon_order_id",
            order_by_clause="amazon_order_id ASC, purchase_date ASC",
            sql_filename="amzn_shipment_query"
        )
    elif "shopify" in report_type:
        shipment_report(
            #pdf_path="/home/hari/Desktop/Automation/Test documents/post shipping labes",
            pdf_path=r"D:\6.SPEED POST\1.Shipping labels",
            pattern=post_order_id_pattern,
            fields=""" Name, Financial_Status, Paid_at, Fulfillment_Status, Fulfilled_at, Subtotal, Shipping, Total, Lineitem_quantity, Lineitem_name,
                Lineitem_price, Lineitem_compare_at_price, Shipping_Province_Name,""",
            table="sh_orders",id="name",
            order_by_clause="lineitem_name ASC, lineitem_price ASC",
            sql_filename="post shipment report"
        )
