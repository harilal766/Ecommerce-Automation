from helpers.dir_switcher import *
from helpers.pdf_pattern_finder import *
from helpers.regex_patterns import *
from helpers.excel_to_sql_scripts import *
from helpers.sql_scripts import *
from helpers.file_ops import *
from helpers.messages import *
import sqlite3

from report_generator import *

import pandas as pd
import os
#pdf_pattern_finder(filepath=dir_switch(directory='post_label'),pattern=amazon_order_id_pattern)

"""
    Filepath should be like this r"<path>"
"""
print("Code Testing")

"""
create_table(sql_table_name="Transactions",
             file_path=r"D:\Ecommerce-Automation\Test documents\amazon settlement\Transaction table cod & prepaid.xlsx")
"""

#pdf_pattern_finder(filepath=r"D:\5.Amazon\Mathew global\INvoice",pattern=amazon_order_id_pattern) 

#report_driver("Amazon")



#print(sql_column_creator(filepath=r"D:\Ecommerce-Automation\Test documents\post orders sheet",filename="1.10.24.xlsx"))


#sql_columns_constructor(filepath=r"D:\Ecommerce-Automation\Test documents\post orders sheet\1.10.24.xlsx")
"""
data_import(tablename="Orders",
            sample_filepath=r"D:\Ecommerce-Automation\Test documents\post orders sheet\1.10.24.xlsx",
            input_filepath=r"D:\5.Amazon\Mathew global\Scheduled report")

"""

"""
data_import(tablename="Orders",
    sample_filepath=r"D:\5.Amazon\Mathew global\Scheduled report\order sample table.xlsx",
    input_filepath=r"D:\5.Amazon\Mathew global\Scheduled report",input_filename="1-31.txt")

"""

#shopify_order_excel_sample = r"D:\Ecommerce-Automation\Test documents\post orders sheet\1.10.24.xlsx"

#shopify_order_excel_sample = r"/home/hari/Desktop/Ecommerce-Automation/Test documents/post orders sheet/1.10.24.xlsx"
"""
list = sql_columns_constructor(filepath=shopify_order_excel_sample)

for i in list:
    print(f"{i} - {datatype_finder(i)}")
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
        



# Directories
    #POST
lin_shopify_order_excel_file = r"/home/hari/Desktop/Ecommerce-Automation/Test documents/post orders sheet/1.10.24.xlsx"
win_shopify_cod_order_excel_dir = r"D:\6.SPEED POST\Return Report COD"
    #AMAZON
win_amazon_order_txt_file = r"D:\5.Amazon\Mathew global\Scheduled report"






"""
sql_table_creation_or_updation(dbname="Shopify",tablename="cod_orders",
                               replace_or_append="replace",
                               input_file_dir=win_shopify_cod_order_excel_dir)
"""

sql_table_creation_or_updation(dbname="Amazon",tablename="Orders",
                               replace_or_append='replace',
                               input_file_dir=win_amazon_order_txt_file)
