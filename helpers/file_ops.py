import os
from .messages import better_error_handling,status_message
def filepath_constructor(filepath,filename):
    filepath = os.path.join(filepath,filename)
    return filepath


def input_handling(instruction):
    try:
        return instruction
    except KeyboardInterrupt as ki:
        print("Interrupted.")


def input_checker(display_message,filepath):
    while True:
        try:
            file = input(display_message)
            if f"{file}.pdf" not in os.listdir(filepath):
                status_message(message="File Not Found, Try again.",color='red')
            else:
                status_message(message="File Found.",color='green')
                break
        except KeyboardInterrupt:
            status_message(message="Keyboard Interruption, Try again.",color='red')
    return file


import pdfplumber
import re
import os
from .messages import *
from .dir_switcher import dir_switch
from .regex_patterns import amazon_order_id_pattern
from .file_ops import *



# need Seperate function for file selection
def pdf_pattern_finder(filepath,pattern):
    pattern_list = []
    filename = None
    status_message(message=f"Filepath : {filepath}",color='blue')
    try:
        filename = input_checker(display_message="Enter pdf the filename : ",filepath=filepath)
        if filename:
            file_path = os.path.join(filepath, f"{filename}.pdf")
            success_status_msg("File Accessed.")
        else:
            print("Enter a filename : ")

        with pdfplumber.open(file_path) as pdf:
            success_status_msg("Opening the pdf file")
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
        success_status_msg(f"Total {len(pattern_list)} Patterns Found in the file : {filename}.pdf\n{pattern_list}")
        return pattern_list

