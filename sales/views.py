from django.shortcuts import render
from amazon.response_manipulator import amazon_dashboard
from amazon.api_models import Orders
from datetime import datetime,timedelta

# Create your views here.

def home(request):
    ord_ins = Orders(); created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()
    ord_resp = ord_ins.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")
    summary = amazon_dashboard(response=ord_resp)
    context = {
        'total_orders' : summary[0],
        'ship_dates' : summary[1]
        }
    return render(request,'home.html',context)
