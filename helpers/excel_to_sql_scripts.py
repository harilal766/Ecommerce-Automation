import pandas as pd

def datatype_finder(column):
    types = {
        # There should be atlest 2 strings on the tuple
        ("phone","mobile"): "VARCHAR(15)",
        ("id","status"): "VARCHAR(20)",
        ("is","will","accepts"): "BOOLEAN NOT NULL",
        ("date","at"): "TIMESTAMP",
        ("quantity", "subtotal", "number"): "INTEGER",
        ("price","taxes", "discount", "amount","total"): "NUMERIC(10,2)",
        ("city","state","address"): "VARCHAR(100)",
        ("zip","postal"): "CHAR(6)"
    }
    # Check if the column name contains any of the key elements
    column = column.lower()
    for keys, value in types.items():
        for key in keys:
            col_last_word = column.split("_")[-1]
            col_first_word = column.split("_")[0]
            key_last_word = key.split("_")[-1]
            # if last word of column = key, return the associated value
            if (key == col_last_word) or (column == col_last_word) and (col_first_word == key) or (key_last_word in col_last_word):
                return value
            
    # Default type if no match is found
    return "VARCHAR(50)"

# Test the function
print(datatype_finder("price_subtotal"))  # Should return INTEGER






def gdatatype_finder(column_data):
    if pd.api.types.is_integer_dtype(column_data):
        return 'INTEGER'  # You can use BIGINT for larger integers
    elif pd.api.types.is_float_dtype(column_data):
        return 'FLOAT'  # You can use NUMERIC for higher precision
    elif pd.api.types.is_datetime64_any_dtype(column_data):
        return 'TIMESTAMP'
    else:
        return 'TEXT'







def sql_file_creator(table_name,query):
    filename = f'{table_name.capitalize()}-table creation query.txt'
    with open(filename,'w') as query_file:
        query_file.write(query)
        print("File created")


def null_populator():
    pass


def file_route():
    try :
        route = f'D:/Automation/SQL Test/{filename}'
        with open(filename,'r') as input_file:
            print(input_file.read())
    except FileNotFoundError:
        route = f'/run/media/hari/HARI/Python Fullstack/Automation/SQL Test/{filename}'
        if os.path.exists(route):
            input_file = pandas.read_excel(route)
        else:
            print("Excel file not found")
    finally:
        headers = input_file[0]
    # changing null ineger values to zero
    print(headers)