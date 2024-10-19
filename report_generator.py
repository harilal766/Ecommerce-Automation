from helpers.pdf_pattern_finder import *
from helpers.sql_scripts import psql_connector,query_backup
from helpers.loading_animations import loading_animation
from helpers.regex_patterns import *


"""
    make the query for filtering cod and non cod datas from sql

"""

space = "-"*15

        
def shipment_report(pdf_path,pattern,fields,table,id,order_by_clause,sql_filename):
    out_excel_path = None
    order_ids = None
    order_id_list = pdf_pattern_finder(filepath=pdf_path,pattern=pattern)
    try:
        order_ids = ','.join([f"'{order_id}'" for order_id in order_id_list])
        
        shipment_report_query = f"""
            SELECT DISTINCT
            {fields} 
            FROM {table} 
            WHERE {id} IN (
                \t{order_ids}
            )
            {order_by_clause};
        """
        #loading_animation(len(order_ids))
        # Backing up the query
        print(shipment_report_query)
        query_backup(f"{sql_filename}",shipment_report_query)

    except Exception:
        pass


shipment_report(
    pdf_path="D:\6.SPEED POST\1.Shipping labels",pattern=post_order_id_pattern,
    fields="name,paid_at,fulfillment_status,subtotal,shipping,taxes,total,lineitem_quantity,lineitem_name,lineitem_price,lineitem_compare_at_price",
    table="sh_orders", id = "name",
    order_by_clause= "ORDER BY lineitem_name ASC, lineitem_price ASC",
    sql_filename="amzn_shipment_query"
    )