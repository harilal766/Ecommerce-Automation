#$import psycopg2
import pandas as pd
import os
from .messages import better_error_handling,success_status_msg,color_text
from .file_ops import *
import calendar,time
from datetime import datetime
import  calendar 
import pg8000,sqlite3
from sqlalchemy import create_engine
import pandas as pd

def db_connection(dbname,db_system):
    function_boundary(title="DB CONNECTION")
    try:
        if db_system == "postgres":
            connection = pg8000.connect(
                user='postgres',
                password='1234',
                host='localhost',      
                port=5432,            
                database=dbname
                )
        elif db_system == "sqlite":
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
    
def sql_to_excel(sql_cursor,query_result,out_excel_path):
    function_boundary(title="SQL 2 EXCEL CONVERSION")
    try:  
        success_status_msg("Excel conversion Started.")
        # excel conversion
        # replacing underscores with empty spaces in columns
        column_list = [desc[0].replace("_"," ") for desc in sql_cursor.description]
        excel_sheet = pd.DataFrame(query_result,columns=column_list)
        # if the excel file already exists, a sheet should be created inside the file and the output should be stored there.
        out_excel_file = input("Enter the name of the output excel file : ")
        if len(out_excel_file) > 0:
            # re initialization of the file path after getting the filename
            out_directory = out_excel_path
            out_excel_path = os.path.join(out_directory,out_excel_file+".xlsx")
            excel_sheet.to_excel(out_excel_path,index="False",engine='openpyxl')
            if out_excel_file in os.listdir(out_directory):
                success_status_msg(f"Excel output file : {out_directory} created.")
        else:
            print("Please enter the filename..")
    except Exception as e:
        better_error_handling(e)

def sql_table_CR(dbname,tablename,replace_or_append,input_file_dir,filename=None):
    try:
        connection = db_connection(dbname=dbname,db_system="sqlite")
        if filename != None:
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
        elif extension == "tsv":
            df = pd.read_csv(filepath,sep='\t')
        else:
            print("UNSUPPORTED EXTENSION")
        
        # replacing " " with "-"
        df.columns = df.columns.str.replace(' ', '_').str.replace("-","_")
        
        engine = create_engine(f'sqlite:///{dbname}.db')
        df.to_sql(tablename,con=engine, if_exists=str(replace_or_append), index=False)
    except FileNotFoundError:
        color_text(message=f"{filename} not found, if the name is correct, please check the spaces....",color='red')
    except Exception as e:
        better_error_handling(e)
    finally:
        connection.close()
        color_text(message="Connection closed.",color="green")