import os
from .messages import better_error_handling,color_print
import platform
import pdfplumber
import re
import os,json
from .messages import *
from .regex_patterns import amazon_order_id_pattern
from .file_ops import *
from pathlib import Path

# Directories
    #POST
win_shopify_invoice = r"D:\6.SPEED POST\1.Shipping labels"
lin_shopify_invoice = r"/home/hari/Desktop/Ecommerce-Automation/Test documents/post shipping labes"

win_shopify_order_excel_file = r"D:\3.Shopify\Date wise order list"
lin_shopify_order_excel_file = r"/home/hari/Desktop/Ecommerce-Automation/Test documents/post orders sheet/1.10.24.xlsx"

win_shopify_cod = r"D:\6.SPEED POST\Return Report COD tallying"
lin_shopify_cod = r"/home/hari/Desktop/Ecommerce-Automation/Test documents/Return Report COD"
    #AMAZON
win_amazon_order_txt = r"D:\5.Amazon\Mathew global\Scheduled report"

win_amazon_invoice = r"D:\5.Amazon\Mathew global\INvoice"
lin_amazon_invoice =r"/home/hari/Desktop/Ecommerce-Automation/Test documents/amazon shipping label"

win_amazon_scheduled_report = r"D:\5.Amazon\Mathew global\Scheduled report"
lin_amazon_scheduled_report = r"/home/hari/Desktop/Ecommerce-Automation/Test documents/amazon scheduled report"

win_api_config = r"D:\Ecommerce-Automation\amazon\time_limits.json"
lin_api_config = r"/home/hari/Desktop/Ecommerce-Automation/amazon/time_limits.json"

win_amazon_return = r"D:\5.Amazon\Mathew global\Return"

win_env = r"D/Ecommerce-Automation/.env"
lin_env = r"/home/hari/Desktop/Ecommerce-Automation/.env"


def function_boundary(title):
    dash = "-"*15
    print(f"{dash}{title}{dash}")

def dir_switch(win,lin):
    try:
        operating_sys = (platform.system()).lower()
        if operating_sys == "windows":
            return win
        elif operating_sys == "linux":
            return lin 
    except Exception as e:
        better_error_handling(e)

def filepath_constructor(filepath,filename):
    filepath = os.path.join(filepath,filename)
    return filepath



# change to file_input_checker
def input_checker(display_message,filepath):
    function_boundary(title='INPUT CHECK')

    # displaying the available files in a last in first out order
    color_print(message=f"Filepath : {filepath}",color='blue')
    files_list = [f for f in Path(filepath).iterdir() if f.is_file()]
    recently_added = sorted( files_list, key=os.path.getctime,reverse=True)
    recently_added = [file.name for file in recently_added]
    print(f"Recently Added  Files : {recently_added}")
    available_files = sorted((os.listdir(filepath)))

    while True:
        try:
            file = input(display_message)
            if f"{file}" not in available_files:
                color_print(message="File Not Found, Try again.",color='red')
            else:
                color_print(message="File Found.",color='green')
                break
        except KeyboardInterrupt:
            color_print(message="Keyboard Interruption, Try again.",color='red')
    return file


def text_input_checker(display_message,input_pattern):
    color_print(message=f"Input pattern : {input_pattern}",color='blue')
    while True:
        try:
            input_text = input(display_message)
            if not re.match(input_pattern,input_text):
                color_print(message="Invalid input found.",color="red")
            else:
                success_status_msg("Pattern verified...")
                return input_text
                
        except KeyboardInterrupt:
            color_print(message="Keyboard Interruption, Try again.",color='red')
        
        



# need Seperate function for file selection
def pdf_pattern_finder(message,filepath,pattern):
    function_boundary(title="PDF PATTERN FINDER")
    pattern_list = []
    try:
        filename = input_checker(display_message=f"{message} : ",filepath=filepath)
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
                        color_print(message=f"patterns found on page {page_count} : {result}",color='green')
                        for id in result:
                            pattern_list.append(id)
                    elif len(result) == 0:
                        color_print(message=f"No patterns found on page {page_count}.",color='red')
            success_status_msg(f"Total {len(pattern_list)} Patterns Found in the file : {filename}\n{pattern_list}")

    except Exception as e:
        print(e)
    finally:
        success_status_msg(f"Total {len(pattern_list)} Patterns Found in the file : {filename}\n{pattern_list}")
        return pattern_list

def json_updater(field,updated_value,filepath):
    try:
        function_boundary(title="Json Updater")
    # file loading.
        with open (filepath,'r+') as file:
            data = json.load(file)
            if field not in data.keys():
                color_print(message="This field does not exist.",color='red')
            else:
                color_print(message=f"current value -> {data}",color='blue')
                data[field] = updated_value
                color_print(message=f"updation : {data}",color='blue')
                with open (filepath,'w') as file:
                    json.dump(data,file,indent=4)
            # updation
    except Exception as e:
        better_error_handling(e)



def file_updater(filepath):
    with open(filepath,'r') as file:
        for line in file:
            print(line)


