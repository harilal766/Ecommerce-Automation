import pdfplumber
import re
import os
from .messages import better_error_handling,success_status_msg
from .dir_switcher import dir_switch
from .regex_patterns import amazon_order_id_pattern


# need Seperate function for file selection
def pdf_pattern_finder(filepath,pattern):
    try:
        pattern_list = []
        
        filename = input("Enter pdf filename : ")

        file_path = os.path.join(filepath, f"{filename}.pdf")
        print("File Accessed.")

        with pdfplumber.open(file_path) as pdf:
            print("Opening the pdf file")
            page_count =0
            for page in pdf.pages:
                page_text = page.extract_text()
                page_count+=1
                if page_text:
                    print(f"Opening page {page_count}.",end=" - ")
                    result = re.findall(pattern,page_text)
                    # a single page can have one pattern or more than one pattern, so.............
                    # amazon label have 1 pattern per page and post lable have 4 patterns per page
                    if type(result) == list:
                        print(f"patterns found on page{page_count} : {result}")
                        for id in result:
                            pattern_list.append(id)
                    elif type(result) == int:
                        print("Non List pattern Found")

    except Exception as e:
        print(e)
    finally:
        success_status_msg(f"Total {len(pattern_list)} Patterns Found in the file : {filename}.pdf\n{pattern_list}")
        return pattern_list

