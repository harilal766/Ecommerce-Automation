import psycopg2
import pandas as pd
import os
from helpers.messages import better_error_handling,success_status_msg
"""
https://www.geeksforgeeks.org/postgresql-connecting-to-the-database-using-python/
"""

def psql_connector(dbname):
    try:
        connection = psycopg2.connect(
            user = "postgres",
            password = "1234",
            host = "localhost",
            port = "5432",
            database = dbname
        )
        if connection:
            success_status_msg("Connected to database.")
    except Exception as e:
        better_error_handling(e)
    return connection
    

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

def sql_to_excel(query,dbname):
    """
    check if the file is alredy present
        if not create the file
        anyway, go inside the file and create a sheet for the report.
        prompt the user for a sheetname
        store the data on that sheet.
    save the query to excel
    """
    try:
        # Connect to the database.
        connection = psql_connector(dbname)
        # read the query 
        excel_out = pd.read_sql_query(query,connection)
        print(excel_out)
        # ask the user for excel file name
        out_excel_name = input("Enter Output Excel file name : ")+".xlsx"
        out_directory = f"D:\5.Amazon\Mathew global\Scheduled report"


        out_excel_path = os.path.join(out_directory,out_excel_name)
        excel_out.to_excel(out_excel_path,index=False)
    except Exception as e:
        print(e)
    finally:
        if excel_out:
            print(f"Report saved to {out_excel_path}")
        else:
            print("excel not saved...")



