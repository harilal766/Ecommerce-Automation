#$import psycopg2
import pandas as pd
import os
from .messages import better_error_handling,success_status_msg
import calendar,time
import pg8000,sqlite3
"""
https://www.geeksforgeeks.org/postgresql-connecting-to-the-database-using-python/
"""
def db_connection(dbname,db_system):
    try:
        if db_system == "psql":
            connection = pg8000.connect(
                user='postgres',
                password='1234',
                host='localhost',      
                port=5432,            
                database=dbname
                )
        elif db_system == "sqlite3":
            connection = sqlite3.connect(f"{dbname}.db")
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


def order_table_updation():
    table_name = "Orders"
    field = "purchase_date"
    date = "2024-09-30" 
    try:
        # find the date of last month's last day.
        # connect to the db
        # delete old data
        # ask user for the updated txt name 
        # if the txt file exists
            # import the txt file data to sql table
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
        