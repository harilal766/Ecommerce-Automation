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











#sql_table_creation_or_updation(dbname="Shopify",tablename="cod_oorja",replace_or_append="replace",input_file_dir=dir_switch(win=win_shopify_cod,lin=lin_shopify_cod))




input_checker(display_message="--------",filepath=win_amazon_invoice)