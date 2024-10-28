#$import psycopg2
import pandas as pd
import os
from .messages import better_error_handling,success_status_msg
import calendar
"""
https://www.geeksforgeeks.org/postgresql-connecting-to-the-database-using-python/
"""

    

def query_backup(filename,query):
    with open(f"{filename}.sql",'w') as query_backup:
        query_backup.write(query)
        print("Query Backed Up.")


def line_limit_checker(word_count,line_limit):
    if word_count % line_limit == 0:
        return True
    return False


def order_table_updation(tablename,filepath,input_filename):
    table_name = "Orders"
    field = "purchase_date"
    date = "2024-09-30" 
    try:
        updation_query = f"""
        /* Deletion of data */
        DELETE FROM {table_name} WHERE {field} > '{date}';
        /* Confirmation */
        SELECT * FROM {table_name} WHERE {field} > '{date}';
        """
        query_backup(filename="order table updation",query=updation_query)
    except Exception as e:
        better_error_handling(e)
    finally:
        print(updation_query)

    # findout last months last date 
    # change the query based on it
    # delete the datas of this month
    # find the txt file with todays updated orders
    # import the data

    import_query = f""" 
        copy Orders (
            amazon_order_id, merchant_order_id, purchase_date, last_updated_date, order_status, fulfillment_channel, sales_channel, order_channel, url, ship_service_level, product_name, sku, asin, item_status, quantity, currency, item_price, item_tax, shipping_price, shipping_tax, gift_wrap_price, gift_wrap_tax, item_promotion_discount, ship_promotion_discount, ship_city, ship_state, ship_postal_code, ship_country, promotion_ids, is_business_order, purchase_order_number, price_designation, is_iba
            ) 
        FROM 'D:/Automation/SQL Test/Order table txt/Orders 1.10.24 - 7.10.24.txt' 
        WITH (
            FORMAT text,
            DELIMITER E'\t',
            ENCODING 'UTF8',
            NULL 'null'
        );
    """
    
    
