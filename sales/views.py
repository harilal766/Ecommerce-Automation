from django.shortcuts import render
from amazon.response_manipulator import sp_api_shipment_summary
from amazon.api_models import Orders
from datetime import datetime,timedelta
# Create your views here.

def home(request):
    ord_ins = Orders(); created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()
    ord_resp = ord_ins.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")
    context = {
        'total_orders' : sp_api_shipment_summary(response=ord_resp)[0],
        'ship_dates' : sp_api_shipment_summary(response=ord_resp)[1]
        }
    return render(request,'home.html',context)
