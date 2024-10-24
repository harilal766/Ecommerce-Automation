from helpers.dir_switcher import dir_switch
from helpers.pdf_pattern_finder import pdf_pattern_finder
from helpers.regex_patterns import amazon_order_id_pattern
import os

#pdf_pattern_finder(filepath=dir_switch(directory='post_label'),pattern=amazon_order_id_pattern)

"""
    Filepath should be like this r"<path>"
"""


filepath = dir_switch(directory="post_label")
print(f" filepath :{filepath}")
files = os.listdir(fr"{filepath}")
print(files)


