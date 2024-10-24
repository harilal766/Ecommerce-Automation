import psycopg2
import pandas as pd
import os
from helpers.messages import better_error_handling,success_status_msg
"""
https://www.geeksforgeeks.org/postgresql-connecting-to-the-database-using-python/
"""

    

def column_underscore(column):
    return column.replace(" ","_")

def query_backup(filename,query):
    with open(f"{filename}.sql",'w') as query_backup:
        query_backup.write(query)
        print("Query Backed Up.")


def line_limit_checker(word_count,line_limit):
    if word_count%line_limit == 0:
        return True
    return False



