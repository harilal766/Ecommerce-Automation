from helpers.file_ops import *
import requests
from amazon.authorization import get_or_generate_access_token,get_or_generate_access_token
from datetime import datetime


from amazon.order_table_updater import Reports


ins = Reports()

rep = ins.createReport(reportType="GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL")
print(rep)

