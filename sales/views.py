from django.shortcuts import render
from amazon.response_manipulator import amazon_dashboard
from amazon.api_models import Orders,Reports
from datetime import datetime,timedelta
from amazon.response_manipulator import *

# Create your views here.

def home(request):
    ord_ins = Orders(); created_after = (datetime.utcnow() - timedelta(days=4)).isoformat()
    ord_resp = ord_ins.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")
    summary = amazon_dashboard(response=ord_resp)
    context = {
        'shipment_summary' : summary
        }
    return render(request,'home.html',context)

def amazon_reports(request):
    R = Reports()
    df = sp_api_report_df_generator(report_type=order_report_types["datewise orders data flatfile"],
                                start_date=iso_8601_timestamp(5),end_date=iso_8601_timestamp(0))
    df.to_sql(name="Amazon",con=db_connection(dbname="Orders",db_system="sqlite"),
                  if_exists='replace',index=False)
    
    context = {"df" : df}
    return render(request,'amazon_reports.html',context)
