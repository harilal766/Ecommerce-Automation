import pandas as pd
from helpers.messages import better_error_handling,success_status_msg
from helpers.sql_scripts import query_backup,line_limit_checker,column_underscore

def datatype_finder(column):
    types = {
        # There should be atlest 2 strings on the tuple
        ("phone","mobile"): "VARCHAR(15)",
        ("id","status"): "VARCHAR(20)",
        ("is","will","accepts"): "BOOLEAN NOT NULL",
        ("date","at"): "TIMESTAMP",
        ("quantity", "subtotal", "number"): "INTEGER",
        ("price","taxes", "discount", "amount","total","fees"): "NUMERIC(10,2)",
        ("city","state","address"): "VARCHAR(100)",
        ("zip","postal"): "CHAR(6)"
    }
    # Check if the column name contains any of the key elements
    column = column.lower()
    for keys, value in types.items():
        for key in keys:
            col_last_word = column.split("_")[-1]
            col_first_word = column.split("_")[0]
            #print(column.split("_"))
            if (key == col_last_word):
                return value
            elif key == col_first_word:
                return value
            elif (key in column):
                return value
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


def create_table(sql_table_name,file_path):
    try:
        # open the file 
        excel = pd.read_excel(file_path,header=0)
        excel_first_row = excel.iloc[0]
        excel_header = excel.columns
        success_status_msg("Filepath read successfully")
        
        #loop columns and replace " " with "_"
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

