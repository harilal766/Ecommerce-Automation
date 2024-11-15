from helpers.file_ops import text_input_checker
import re
from helpers.regex_patterns import post_track_id_pattern,post_order_id_pattern
from helpers.sql_scripts import db_connection
from helpers.messages import color_print
# combine connection and querying into one function..
def db_querying(connection,query):
    if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
    else:
         color_print(message="Connection failed.",color='red')
    return results
        

def post_tracking():
    input_id = input("Enter the ID : ")
    tracking_id = ''
    if re.match(post_track_id_pattern,input_id):
        color_print(message=f"Tracking id found....",color='green')
        tracking_id = input_id
    elif re.match(post_order_id_pattern,input_id):
        pass
        connection = db_connection(dbname='C:\Program Files (x86)\Tejas\master.db',db_system='sqlite')
        barcode_query = f"SELECT barcode from Kalan_Ayur_Products_Orders where barcode = {input_id};"
        result = db_querying(connection=connection,query=barcode_query)
        print(result)
    # Access tejs db and find the barcode
    ship24_track = f"https://www.ship24.com/tracking?p={tracking_id}&a=947"
    indiapost_track = f"https://api.cept.gov.in/CustomTracking/TrackConsignment.asmx/ArticleTracking?Article={tracking_id}&requestingApplication=Cust0M$Tr%40ck"

    tracking_link = ship24_track
    print(f"Ship 24 :\n{tracking_link}\nIndiapost :\n{indiapost_track}")


