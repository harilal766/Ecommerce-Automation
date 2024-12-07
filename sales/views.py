from django.shortcuts import render
from amazon.response_manipulator import amazon_dashboard
from amazon.sp_api_models import Orders,Reports
from datetime import datetime,timedelta
from amazon.response_manipulator import *
from helpers.sql_scripts import *
from django.http import HttpResponse

# Create your views here.
    
def home(request):
    try:
        # initializing context with none, for handling errors 
        context = {'shipment_summary' : None, "ship_date": None}
        orders_instance = Orders(); created_after = (datetime.utcnow() - timedelta(days=4)).isoformat()
        ord_resp = orders_instance.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")
        if ord_resp != None:
            summary = amazon_dashboard(response=ord_resp)
            context["shipment_summary"] = summary
            context["ship_date"] = amzn_next_ship_date().split("T")[0]
        else:
            color_text(message="Empty response from getOrders",color="red")
        return render(request,'home.html',context)
    except Exception as e:
        better_error_handling(e)

def amazon_shipment_report(request):
    context = {"path" : None}
    try:
        # fetch the order api and check if there are any orders for todays shipdate
        order_instance = Orders()
        orders = order_instance.getOrders(CreatedAfter=from_timestamp(5),OrderStatuses="Unshipped",LatestShipDate=iso_8601_timestamp(0).split("T")[0])
        if orders == None:
            color_text(message="There are no orders scheduled for today",color="red")
        else:
            pass 

        return render(request,"amazon_reports.html",context)
    
    # if not , stop the program
    except Exception as e:
        better_error_handling(e)