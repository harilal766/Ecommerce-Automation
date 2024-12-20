import pandas as pd
from helpers.messages import better_error_handling,success_status_msg
from helpers.sql_scripts import query_backup,line_limit_checker

def datatype_finder(column):
    # dive in to the non header rows of an excel file
    # if data is string type,
        # read all the datas in that row and find the maximum length
    types = {
        # There should be atlest 2 strings on the tuple
        ("phone","mobile"): "VARCHAR(15)",
        ("id","status"): "VARCHAR(20)",
        ("is","will","accepts"): "BOOLEAN",
        ("date","at"): "TIMESTAMP",
        ("quantity", "subtotal", "number"): "INTEGER",
        ("price","taxes", "discount", "amount","total","fees"): "NUMERIC(10,2)",
        ("city","state","address","street"): "VARCHAR(100)",
        ("zip","postal"): "CHAR(6)"
    }
    # Check if the column name contains any of the key elements
    # Make sure the last word of the column is a string.
    col_last_word = str(column.split("_")[-1].lower())
    for key_tuple in types:
        if (col_last_word in key_tuple):
            return (types.get(key_tuple))
        else:
            return "VARCHAR(50)"
            #return "---------"

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





def create_table_from_excel(sql_table_name,file_path):
    try:
        # open the file 
        excel = pd.read_excel(file_path,header=0)
        excel_first_row = excel.iloc[0]
        excel_header = excel.columns
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
