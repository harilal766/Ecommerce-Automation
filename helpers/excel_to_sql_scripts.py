import pandas as pd
from helpers.messages import better_error_handling,success_status_msg
from helpers.sql_scripts import query_backup,line_limit_checker

def datatype_finder(column):
    # dive in to the non header rows of an excel file
    # if data is string type,
        # read all the datas in that row and find the maximum length
    
    potential_numbers = ["price","taxes", "discount", "amount","total","fees","quantity",
     "subtotal", "number"]
    types = {
        # There should be atlest 2 strings on the tuple
        
        ("phone","mobile"): "VARCHAR(15)",
        ("id","status"): "VARCHAR(20)",
        ("is","will","accepts"): "BOOLEAN",
        ("date","at"): "TIMESTAMP",
        ("quantity", "subtotal", "number"): "NUMERIC(10,2)",
        ("price","taxes", "discount", "amount","total","fees"): "NUMERIC(10,2)",
        ("city","state","address"): "VARCHAR(100)",
        ("zip","postal"): "CHAR(6)"
    }
    # Check if the column name contains any of the key elements
    column = column.lower()
    col_last_word = column.split("_")[-1]
    col_first_word = column.split("_")[0]
    for keys, value in types.items():
        for key in keys:
            #print(column.split("_"))
            if (key == str(col_last_word)):
                return value
                break
    # Default type if no match is found
    return "VARCHAR(50)"
    #return "---------"

def gdatatype_finder(column_data):
    if pd.api.types.is_integer_dtype(column_data):
        return 'INTEGER'  # You can use BIGINT for larger integers
    elif pd.api.types.is_float_dtype(column_data):
        return 'FLOAT'  # You can use NUMERIC for higher precision
    elif pd.api.types.is_datetime64_any_dtype(column_data):
        return 'TIMESTAMP'
    else:
        return 'TEXT'

def column_underscore(column):
    if "-" in column:
        return column.replace("-","_")
    else:
        return column.replace(" ","_")



# Move this function to excel scripts module
def sql_columns_constructor(filepath):
    try:
        excel = pd.read_excel(filepath,header=0)
        excel_first_row = excel.iloc[0]
        excel_header = []
        for column in excel.columns:
            excel_header.append(column_underscore(column))
    except Exception as e:
        better_error_handling(e)
    finally:
        if excel_header:
            return excel_header





def create_table(sql_table_name,file_path):
    try:
        # open the file 
        excel = pd.read_excel(file_path,header=0)
        excel_first_row = excel.iloc[0]
        excel_header = excel.columns
        print(excel_header)
        if not excel.empty:
            success_status_msg("Filepath read successfully.")
        else:
            better_error_handling("Unable to open the excel file.")
        col_with_type = ""
        last_column = list(excel_header)[-1]
        column_count = 0
        for column in excel_header:
            column_count +=1
            if line_limit_checker(word_count=column_count,line_limit=4):
                col_with_type += f"\t{column_underscore(column)} {datatype_finder(column)},\n"
            # avoiding comman at the last column addition
            elif column == last_column:
                col_with_type += f"\t{column_underscore(column)} {datatype_finder(column)}"
            else:
                col_with_type += f"\t{column_underscore(column)} {datatype_finder(column)},"
            

        table_creation_query = f"""
            CREATE TABLE {sql_table_name} (
                {col_with_type}
            );
        """
        query_backup(filename="post order table creation",query=table_creation_query)
        # connect the db , execute the query, try adding the sample data
        #psql_connector(sql_table_name)
    except Exception as e:
        better_error_handling(e)
    finally:
        pass
        success_status_msg(table_creation_query)
