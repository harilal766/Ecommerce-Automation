#$import psycopg2
import pandas as pd
import os
from .messages import better_error_handling,success_status_msg
import calendar
"""
https://www.geeksforgeeks.org/postgresql-connecting-to-the-database-using-python/
"""

    

def column_underscore(column):
    return column.replace(" ","_")

def query_backup(filename,query):
    with open(f"{filename}.sql",'w') as query_backup:
        query_backup.write(query)
        print("Query Backed Up.")


def line_limit_checker(word_count,line_limit):
    if word_count%line_limit == 0:
        return True
    return False


def order_table_updation():
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
    
    
