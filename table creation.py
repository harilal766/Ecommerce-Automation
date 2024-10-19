from helpers.excel_to_sql_scripts import datatype_finder
import pandas as pd
from helpers.messages import better_error_msg,success_status_msg
from helpers.sql_scripts import query_backup

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
        for column in excel_header:
            if column == last_column:
                col_with_type += f"\t{column.replace(' ', '_')} {datatype_finder(column)}"
            else:
                col_with_type += f"\t{column.replace(' ', '_')} {datatype_finder(column)},\n"
        
        table_creation_query = f"""
            CREATE TABLE {sql_table_name} (
                {col_with_type}
            );
        """
        query_backup(filename="post order table creation",query=table_creation_query)

    except Exception as e:
        better_error_msg(e)
    finally:
        pass
        success_status_msg(table_creation_query)



# Shopify orders -> sql
#create_table(table_name="sh_orders",file_route="D:/6.SPEED POST/28.9.24.xlsx")
create_table(sql_table_name="sh_orders",file_path="/home/hari/Desktop/Automation/Test documents/post orders sheet/1.10.24.xlsx")
