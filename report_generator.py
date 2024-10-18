from helpers.pdf_pattern_finder import *
from helpers.sql_scripts import psql_connector,query_backup
from helpers.loading_animations import loading_animation



"""
    make the query for filtering cod and non cod datas from sql

"""
amazon_order_id_pattern = r"\d{3}-\d{7}-\d{7}"
space = "-"*15



post_order_id_pattern = '#\d{5}'
def amazon_shipment_report():
    out_excel_path = None
    order_ids = None
    order_id_list = pdf_pattern_finder(filepath="D:\5.Amazon\Mathew global\INvoice",pattern=post_order_id_pattern)
    try:
        fields = "amazon_order_id,purchase_date,last_updated_date,order_status,product_name, quantity,item_price,item_tax,shipping_price,shipping_tax"
        table = "orders"

        order_ids = ','.join([f"'{order_id}'" for order_id in order_id_list])
        
        shipment_report_query = f"""
            SELECT DISTINCT
            {fields} 
            FROM {table} 
            WHERE amazon_order_id IN (
                \t{order_ids}
            )
            ORDER BY product_name ASC, item_price ASC
            ;
        """
        #loading_animation(len(order_ids))
        # Backing up the query
        query_backup("amzn_shipment_query",shipment_report_query)

    except Exception:
        pass
        
        
def shopify_shipment_report():
    out_excel_path = None
    order_ids = None
    order_id_list = post_pdf_pattern_finder(filepath="D:\6.SPEED POST\1.Shipping labels",pattern=amazon_order_id_pattern)
    try:
        fields = "amazon_order_id,purchase_date,last_updated_date,order_status,product_name, quantity,item_price,item_tax,shipping_price,shipping_tax"
        table = "sh_orders"
        order_ids = ','.join([f"'{order_id}'" for order_id in order_id_list])
        
        shipment_report_query = f"""
            SELECT DISTINCT
            {fields} 
            FROM {table} 
            WHERE amazon_order_id IN (
                \t{order_ids}
            )
            ORDER BY product_name ASC, item_price ASC
            ;
        """
        #loading_animation(len(order_ids))
        # Backing up the query
        print(shipment_report_query)
        query_backup("amzn_shipment_query",shipment_report_query)

    except Exception:
        pass


shopify_shipment_report()