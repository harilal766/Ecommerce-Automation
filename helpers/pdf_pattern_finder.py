import pdfplumber
import re
import os
from messages import better_error_msg,success_status_msg
from dir_switcher import dir_switch

def pdf_pattern_finder(filepath,pattern):
    try:
        pattern_list = []
        filename = input("Enter the pdf filename: ")
        path_with_file = fr"{filepath}\{filename}.pdf"
        with pdfplumber.open(path_with_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                order_ids = re.findall(pattern, page_text)
                for order_id in order_ids:
                    pattern_list.append(order_id)
    except FileNotFoundError:
        print(f"This file does not exist")
    finally:
        print(f"{len(pattern_list)} orders found\n")
        return pattern_list




def post_pdf_pattern_finder(filepath,pattern):
    try:
        pattern_list = []
        filename = input("Enter pdf filename : ")
        file_path = os.path.join(filepath, f"{filename}.pdf")
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    result = re.findall(pattern,page_text)
                    # a single page can have one pattern or more than one pattern, so.............
                    if type(result) == list:
                        for id in result:
                            pattern_list.append(id)
                    elif type(result) == int:
                        pass

                else:
                    print(f"No text found at {filename}.pdf")

    except Exception as e:
        better_error_msg(e)
    finally:
        success_status_msg(f"{len(pattern_list)} Patterns Found in the file : {filename}.pdf\n{pattern_list}")
        return pattern_list



#post_pdf_pattern_finder(filepath="/home/hari/Desktop/Automation/Test documents/post shipping labes", pattern='#\d{5}')
#pdf_pattern_finder(filepath=r"D:\5.Amazon\Mathew global\INvoice",pattern='\d{3}-\d{7}-\d{7}')
#post_pdf_pattern_finder(filepath=r"D:\6.SPEED POST\1.Shipping labels",pattern='#\d{5}')