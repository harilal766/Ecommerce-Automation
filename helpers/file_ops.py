import os
from .messages import better_error_handling,status_message
import platform
import pdfplumber
import re
import os
from .messages import *
from .regex_patterns import amazon_order_id_pattern
from .file_ops import *

# Directories
    #POST
win_shopify_invoice = r"D:\6.SPEED POST\1.Shipping labels"
lin_shopify_invoice = r"/home/hari/Desktop/Ecommerce-Automation/Test documents/post shipping labes"

win_shopify_order_excel_file = r"D:\3.Shopify\Date wise order list"
lin_shopify_order_excel_file = r"/home/hari/Desktop/Ecommerce-Automation/Test documents/post orders sheet/1.10.24.xlsx"

win_shopify_cod = r"D:\6.SPEED POST\Return Report COD"
lin_shopify_cod = r"/home/hari/Desktop/Ecommerce-Automation/Test documents/Return Report COD"
    #AMAZON
win_amazon_order_txt = r"D:\5.Amazon\Mathew global\Scheduled report"

win_amazon_invoice = r"D:\5.Amazon\Mathew global\INvoice"
lin_amazon_invoice =r"/home/hari/Desktop/Ecommerce-Automation/Test documents/amazon shipping label"

win_amzn_scheduled_report = r"D:\5.Amazon\Mathew global\Scheduled report"
lin_amzn_scheduled_report = r""


def function_boundary(title):
    dash = "-"*15
    print(f"{dash}{title}{dash}")

def dir_switch(win,lin):
    if platform == "windows":
        return win
    elif platform == "Linux":
        return lin 

def filepath_constructor(filepath,filename):
    
    filepath = os.path.join(filepath,filename)
    return filepath




def input_checker(display_message,filepath):
    function_boundary(title='INPUT CHECK')
    available_files = sorted((os.listdir(filepath)))
    while True:
        try:
            file = input(display_message)
            if f"{file}" not in available_files:
                status_message(message="File Not Found, Try again.",color='red')
            else:
                status_message(message="File Found.",color='green')
                break
        except KeyboardInterrupt:
            status_message(message="Keyboard Interruption, Try again.",color='red')
    return file




# need Seperate function for file selection
def pdf_pattern_finder(filepath,pattern):
    pattern_list = []
    filename = None
    status_message(message=f"Filepath : {filepath}",color='blue')
    try:
        filename = input_checker(display_message="Enter the filename with extension : ",filepath=filepath)
        if filename:
            file_path = os.path.join(filepath, f"{filename}")
            success_status_msg("File Accessed.")
        else:
            print("Enter a filename : ")

        with pdfplumber.open(file_path) as pdf:
            success_status_msg("Opening the file........")
            page_count =0
            for page in pdf.pages:
                page_text = page.extract_text()
                page_count+=1
                if page_text:
                    success_status_msg(f"Opening page {page_count}.")
                    result = re.findall(pattern,page_text)
                    # a single page can have one pattern or more than one pattern, so.............
                    # amazon label have 1 pattern per page and post lable have 4 patterns per page
                    if result:
                        status_message(message=f"patterns found on page {page_count} : {result}",color='green')
                        for id in result:
                            pattern_list.append(id)
                    elif len(result) == 0:
                        status_message(message=f"No patterns found on page {page_count}.",color='red')

    except Exception as e:
        print(e)
    finally:
        success_status_msg(f"Total {len(pattern_list)} Patterns Found in the file : {filename}\n{pattern_list}")
        return pattern_list

