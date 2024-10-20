import pdfplumber
import re
import os
from .messages import better_error_handling,success_status_msg
from .dir_switcher import dir_switch


def pdf_pattern_finder(filepath,pattern):
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
                    # amazon label have 1 pattern per page and post lable have 4 patterns per page
                    if type(result) == list:
                        print(f"patterns found on page : {result}")
                        for id in result:
                            pattern_list.append(id)
                    elif type(result) == int:
                        print("Non List pattern Found")

    except Exception as e:
        better_error_handling(e)
    finally:
        success_status_msg(f"Total {len(pattern_list)} Patterns Found in the file : {filename}.pdf\n{pattern_list}")
        return pattern_list



#pdf_pattern_finder(filepath="/home/hari/Desktop/Automation/Test documents/post shipping labes", pattern='#\d{5}')
#pdf_pattern_finder(filepath=r"D:\5.Amazon\Mathew global\INvoice",pattern='\d{3}-\d{7}-\d{7}')
#pdf_pattern_finder(filepath=r"D:\6.SPEED POST\1.Shipping labels",pattern='#\d{5}')
