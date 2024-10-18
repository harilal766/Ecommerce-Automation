
# call the code to connect to database

# call the import code

table_name = "Orders"
field = "purchase_date"
date = "2024-09-30"

delete_query = f""" 
        DELETE FROM {table_name} WHERE {field} > '{date}';
"""


confirmation = f"""
    SELECT * FROM {table_name} WHERE {field} > '{date}';
"""


print(f"Delete Query :\n{delete_query}\nConfirmation Query :\n{confirmation}")