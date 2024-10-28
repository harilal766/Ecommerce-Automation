from helpers.dir_switcher import dir_switch
from helpers.pdf_pattern_finder import pdf_pattern_finder
from helpers.regex_patterns import amazon_order_id_pattern
from helpers.excel_to_sql_scripts import create_table
from report_generator import report_driver
from helpers.excel_to_sql_scripts import column_underscore,sql_column_creator
from helpers.file_ops import filepath_constructor
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



print(sql_column_creator(filepath=r"D:\Ecommerce-Automation\Test documents\post orders sheet",filename="1.10.24.xlsx"))