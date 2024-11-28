from amazon.authorization import *
from amazon.api_models import *
from amazon.response_manipulator import *


# item['PaymentMethodDetails']   ['CashOnDelivery']  ['Standard']
"""
ord_ins = Orders(); created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()
ord_resp = ord_ins.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")
color_text(message=ord_resp,color="red")
summary = amazon_dashboard(response=ord_resp)
print(summary)
"""
limit = 3500
print(-limit)

# venv\Scripts\activate

#  D:\Ecom-Dashboard\venv\Scripts\python.exe d:/Ecom-Dashboard/spapi.py