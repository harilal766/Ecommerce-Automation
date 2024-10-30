#$import psycopg2
import pandas as pd
import os
from .messages import better_error_handling,success_status_msg
import calendar,time
import pg8000
"""
https://www.geeksforgeeks.org/postgresql-connecting-to-the-database-using-python/
"""
def psql_db_connection(dbname):
    try:
        connection = pg8000.connect(
            user='postgres',
            password='1234',
            host='localhost',      
            port=5432,            
            database=dbname
            )
    except Exception as e:
        better_error_handling(e)
    finally:
        if connection:
            return connection
        else:
            better_error_handling("Database connection failed")
    

def query_backup(filename,query):
    try:
        with open(f"{filename}.sql",'w') as query_backup:
            query_backup.write(query)
    except Exception as e:
        better_error_handling(e)
    finally:
        success_status_msg("Query Backed Up.")



def line_limit_checker(word_count,line_limit):
    if word_count % line_limit == 0:
        return True
    return False






def data_import(tablename,sample_filepath,input_filepath):
    """ 
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
    # importing only while needed so that circular impoprt error can be avoided.
    from .excel_to_sql_scripts import sql_columns_constructor
    columns = sql_columns_constructor(filepath=sample_filepath)
    data_import_query = f"""COPY {tablename} {columns}
    FROM '{input_filepath}'
    WITH (
    FORMAT,
    DELIMITER,
    ENCODING 'UTF8',
    NULL ''
        );
    """
    print(data_import_query)


def order_table_updation():
    table_name = "Orders"
    field = "purchase_date"
    date = "2024-09-30" 
    deletion_query = f"DELETE FROM {table_name} WHERE {field} > '{date}';"
    confirmation_query = ""
    try:
        # find the date of last month's last day.
        # connect to the db
        # delete old data
        connection = psql_db_connection(dbname="Amazon")

        """
        # ask user for the updated txt name 
        input_file = input("Enter the input txt filename : ")
        # if the txt file exists
        if input_file:
            # import the txt file data to sql table
            pass
        """

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

    
    

    
def sql_to_excel(sql_cursor,query_result,out_excel_path):
    try:  
        # excel conversion
        # replacing underscores with empty spaces in columns
        column_list = [desc[0].replace("_"," ") for desc in sql_cursor.description]
        excel_sheet = pd.DataFrame(query_result,columns=column_list)
        # if the excel file already exists, a sheet should be created inside the file and the output should be stored there.
        out_excel_file = input("Enter the name for excel file : ")
        if out_excel_file:
            # re initialization of the file path after getting the filename
            out_excel_path = os.path.join(out_excel_path,out_excel_file+".xlsx")
            excel_sheet.to_excel(out_excel_path,index="Flase",engine='openpyxl')
            success_status_msg("Excel output created.")
        else:
            print("Please enter the filename..")
    except Exception as e:
        better_error_handling(e)
        