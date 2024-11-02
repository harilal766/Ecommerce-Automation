#$import psycopg2
import pandas as pd
import os
from .messages import better_error_handling,success_status_msg,status_message
from .file_ops import input_handling,input_checker
import calendar,time
from datetime import datetime
import  calendar 
import pg8000,sqlite3
from sqlalchemy import create_engine


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
            success_status_msg(f"Connected to the databse : {dbname}.")
            return connection
        else:
            better_error_handling(f"Connection failed to the database : {dbname}.")
    

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



def data_import(tablename,sample_filepath,input_filepath,input_filename):
    delimiters = {
        "txt": "E'\t'"
    }
         
    # importing only while needed so that circular impoprt error can be avoided.
    from .excel_to_sql_scripts import sql_columns_constructor
    columns = sql_columns_constructor(filepath=sample_filepath)
    data_import_query = f"""COPY {tablename} {tuple(columns)}
    FROM '{os.path.join(input_filepath,input_filename)}'
    WITH (
    FORMAT TEXT,
    DELIMITER E'\t',
    ENCODING 'UTF8',
    NULL ''
        );
    """
    print(data_import_query)



def order_table_updation():
    table_name = "Orders"
    field = "purchase_date"

    # find the date of last month's last day.
    today = datetime.today()
    last_month = today.month-1
    yestermonth_last_day = calendar.month(today.year,today.month)[-3:-1]
    if last_month < 10:
        last_month = f"0{last_month}"
    yestermonth_last_date = f"{today.year}-{last_month}-{yestermonth_last_day}"


    deletion_query = f"DELETE FROM {table_name} WHERE {field} > '{yestermonth_last_date}';"
    try:
        # connect to the db
        connection = db_connection(dbname="Amazon")
        cursor=connection.cursor()
        # delete old data
        cursor.execute(deletion_query)
        # ask user for the updated txt name 
        input_file = input_checker(display_message="Enter the input txt filename : ")
        # if the txt file exists
        if input_file:
            # import the txt file data to sql table
            pass
        

        updation_query = f"""
        /* Deletion of data */
        DELETE FROM {table_name} WHERE {field} > '{yestermonth_last_date}';
        /* Confirmation */
        SELECT * FROM {table_name} WHERE {field} > '{yestermonth_last_date}';
        """
        query_backup(filename="order table updation",query=updation_query)
    except Exception as e:
        better_error_handling(e)
    finally:
        pass


    
def sql_to_excel(sql_cursor,query_result,out_excel_path):
    try:  
        print("Excel conversion Started.")
        # excel conversion
        # replacing underscores with empty spaces in columns
        column_list = [desc[0].replace("_"," ") for desc in sql_cursor.description]
        excel_sheet = pd.DataFrame(query_result,columns=column_list)
        # if the excel file already exists, a sheet should be created inside the file and the output should be stored there.
        out_excel_file = input_handling("Enter the name for excel file : ")
        if out_excel_file:
            # re initialization of the file path after getting the filename
            out_directory = out_excel_path
            out_excel_path = os.path.join(out_directory,out_excel_file+".xlsx")
            excel_sheet.to_excel(out_excel_path,index="Flase",engine='openpyxl')
            if out_excel_file in os.listdir(out_directory):
                success_status_msg(f"Excel output file : {out_directory} created.")
        else:
            print("Please enter the filename..")
    except Exception as e:
        better_error_handling(e)
        

        
def input_sanitizer(instruction,datatype):
    pass



def sql_table_creation_or_updation(dbname,tablename,replace_or_append,input_file_dir):
    success_status_msg("SQL CRUD OPERATIONS")
    try:
        connection = db_connection(dbname=dbname,db_system="sqlite")
        filename = input_checker(display_message="Enter the input filename with extension :- ",filepath=input_file_dir)
        extension = str(filename.split(".")[-1]).lower()
        df = ""
        filepath = os.path.join(input_file_dir,filename)
        
        if extension == "xlsx":
            sheet_name = input("Enter the name of the sheet : ")
            df = pd.read_excel(filepath, sheet_name=sheet_name)
        elif extension == "txt":
            df = pd.read_csv(filepath,delimiter='\t',on_bad_lines='skip')
        elif extension == "csv":
            df = pd.read_csv(filepath,delimiter=',',on_bad_lines='skip')
        else:
            raise ValueError("UNSUPPORTED EXTENSION")
        
        # replacing " " with "-"
        df.columns = df.columns.str.replace(' ', '_').str.replace("-","_")
        
        engine = create_engine(f'sqlite:///{dbname}.db')
        df.to_sql(tablename,con=engine, if_exists=str(replace_or_append), index=False)
    except FileNotFoundError:
        status_message(message=f"{filename} not found, if the name is correct, please check the spaces....",color='red')
    except Exception as e:
        better_error_handling(e)
    finally:
        connection.close()