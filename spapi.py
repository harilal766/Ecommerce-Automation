from amazon.authorization import *
from amazon.api_models import *
from amazon.response_manipulator import *

# item['PaymentMethodDetails']   ['CashOnDelivery']  ['Standard']

ord_ins = Orders()
ord_resp = ord_ins.getOrders(CreatedAfter=iso_8601_timestamp(5),OrderStatuses="Unshipped",
                             PaymentMethods="COD",EarliestShipDate=iso_8601_timestamp(0))

if ord_resp != None:
    for order in ord_resp:
        if type(order) == dict:
            print(f"{order['AmazonOrderId']}\nearliest : {order['EarliestShipDate']}\nlatest : {order['LatestShipDate']}\nlast update : {order['LastUpdateDate']}")
            color_text(message="++++",color='blue')
    print(len(ord_resp))
else:
    color_text(message="Output is None.",color="red")




# venv\Scripts\activate

#  D:\Ecom-Dashboard\venv\Scripts\python.exe d:/Ecom-Dashboard/spapi.py