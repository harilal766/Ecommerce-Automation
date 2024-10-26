from helpers.dir_switcher import dir_switch
from helpers.pdf_pattern_finder import pdf_pattern_finder
from helpers.regex_patterns import amazon_order_id_pattern
import os
from helpers.excel_to_sql_scripts import create_table
from report_generator import report_driver

#pdf_pattern_finder(filepath=dir_switch(directory='post_label'),pattern=amazon_order_id_pattern)

"""
    Filepath should be like this r"<path>"
"""
print("Code Testing")

"""
create_table(sql_table_name="Transactions",
             file_path=r"D:\Ecommerce-Automation\Test documents\amazon settlement\Transaction table cod & prepaid.xlsx")
"""


report_driver("Amazon")