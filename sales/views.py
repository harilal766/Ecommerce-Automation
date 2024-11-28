from django.shortcuts import render
from amazon.response_manipulator import amazon_dashboard
from amazon.api_models import Orders
from datetime import datetime,timedelta

# Create your views here.

def home(request):
    ord_ins = Orders(); created_after = (datetime.utcnow() - timedelta(days=4)).isoformat()
    ord_resp = ord_ins.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")
    summary = amazon_dashboard(response=ord_resp)
    context = {
        'shipment_summary' : summary
        }
    return render(request,'home.html',context)



"" "
1.call order instance 
2. set todays date
3. get cod / prepaid by changing function argument and store into a list or tuple
4. get the df and to sql
5. execute the previously made query. 
" "" 
