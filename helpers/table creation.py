from helpers.excel_to_sql_scripts import datatype_finder
import pandas as pd
from helpers.messages import better_error_handling,success_status_msg
from helpers.sql_scripts import query_backup,psql_connector,line_limit_checker,column_underscore

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
            """
            optimisation
                comma removed column as the basic form
                column with comma
                comma and line break
            """
            """
            col_with_type += f"\t{column_underscore(column)} {datatype_finder(column)}"
            if line_limit_checker(word_count=column_count,line_limit=4):
                col_with_type + ",\n"
            elif not line_limit_checker(word_count=column_count,line_limit=4):
                col_with_type + ","
            """
            if line_limit_checker(word_count=column_count,line_limit=4):
                col_with_type += f"\t{column_underscore(column)} {datatype_finder(column)},\n"
            # avoiding comman at the last column addition
            if column == last_column:
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



