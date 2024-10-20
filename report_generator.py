from helpers.pdf_pattern_finder import *
from helpers.sql_scripts import psql_connector,query_backup
from helpers.loading_animations import loading_animation
from helpers.regex_patterns import *


"""
    make the query for filtering orders form sql table bsaed on seperate cod and non cod pdf files
"""
        
def shipment_report(pdf_path,pattern,fields,table,id,order_by_clause,sql_filename):
    out_excel_path = None
    order_ids = None
    order_id_list = pdf_pattern_finder(filepath=pdf_path,pattern=pattern)
    try:
        order_ids = ""
        for order_id in order_id_list:
            order_ids+= f"'{order_id}',\n"
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
            pdf_path="/home/hari/Desktop/Automation/Test documents/amazon shipping label",
            #pdf_path="D:\6.SPEED POST\1.Shipping labels",
            pattern=amazon_order_id_pattern,
            fields="name,paid_at,fulfillment_status,subtotal,shipping,taxes,total,lineitem_quantity,lineitem_name,lineitem_price,lineitem_compare_at_price",
            table="Orders", id = "amazon_order_id",
            order_by_clause="amazon_order_id ASC, purchase_date ASC",
            sql_filename="amzn_shipment_query"
        )
    elif "shopify" in report_type:
        shipment_report(
            pdf_path="/home/hari/Desktop/Automation/Test documents/post shipping labes",
            #pdf_path="D:\6.SPEED POST\1.Shipping labels",
            pattern=post_order_id_pattern,
            fields="Name, Email, Financial_Status, Paid_at, Fulfillment_Status, Fulfilled_at, Subtotal, Shipping, Total, Lineitem_quantity, Lineitem_name, Lineitem_price, Lineitem_compare_at_price, Billing_Name, Billing_Street, Billing_Address1, Billing_Address2, Billing_Company, Billing_City, Billing_Zip, Billing_Province, Billing_Country, Billing_Phone, Shipping_Name, Shipping_Street, Shipping_Address1, Shipping_Address2, Shipping_Company, Shipping_City, Shipping_Zip, Shipping_Province, Shipping_Country, Shipping_Phone, Location, Device_ID, Id, Tags, Lineitem_discount, Billing_Province_Name, Shipping_Province_Name,",
            table="sh_orders",id="name",
            order_by_clause="lineitem_name ASC, lineitem_price ASC",
            sql_filename="post shipment report"

        )


string = "Name	Email	Financial Status	Paid at	Fulfillment Status	Fulfilled at	Accepts Marketing	Currency	Subtotal	Shipping	Taxes	Total	Discount Code	Discount Amount	Shipping Method	Created at	Lineitem quantity	Lineitem name	Lineitem price	Lineitem compare at price	Lineitem sku	Lineitem requires shipping	Lineitem taxable	Lineitem fulfillment status	Billing Name	Billing Street	Billing Address1	Billing Address2	Billing Company	Billing City	Billing Zip	Billing Province	Billing Country	Billing Phone	Shipping Name	Shipping Street	Shipping Address1	Shipping Address2	Shipping Company	Shipping City	Shipping Zip	Shipping Province	Shipping Country	Shipping Phone	Notes	Note Attributes	Cancelled at	Payment Method	Payment Reference	Refunded Amount	Vendor	Outstanding Balance	Employee	Location	Device ID	Id	Tags	Risk Level	Source	Lineitem discount	Tax 1 Name	Tax 1 Value	Tax 2 Name	Tax 2 Value	Tax 3 Name	Tax 3 Value	Tax 4 Name	Tax 4 Value	Tax 5 Name	Tax 5 Value	Phone	Receipt Number	Duties	Billing Province Name	Shipping Province Name	Payment ID	Payment Terms Name	Next Payment Due At	Payment References"

underscored = string.replace(" ","_")

comma_added = underscored.replace("	",", ")
