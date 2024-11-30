from django.shortcuts import render
from amazon.response_manipulator import amazon_dashboard
from amazon.sp_api_models import Orders,Reports
from datetime import datetime,timedelta
from amazon.response_manipulator import *
from helpers.sql_scripts import *
from django.http import HttpResponse

# Create your views here.
def amzn_next_ship_date(out=None):
    if datetime.now().time().hour >= 11:
    # if the time is past 11:00 AM and todays scheduling is done, return tomorrows date if not a holiday
        return iso_8601_timestamp(-1)
    else:
        return iso_8601_timestamp(0)
    
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

def amazon_reports(request):
    try:
        context = {"path":None}
        orders_instance = Orders()
        orders = orders_instance.getOrders(CreatedAfter=iso_8601_timestamp(4),LatestShipDate=amzn_next_ship_date(),
                                    OrderStatuses="Unshipped")
        cod = [] ; prepaid = []
        for i in orders:
            next_ship_date = datetime.strptime(amzn_next_ship_date().split("T")[0], "%Y-%m-%d")
            latest_ship_date = datetime.strptime(i['LatestShipDate'].split("T")[0], "%Y-%m-%d")
            if isinstance(i,dict):
                if next_ship_date == latest_ship_date:
                    #print(f"{i["AmazonOrderId"]} - {i['LatestShipDate']}")
                    if i["PaymentMethod"] == "COD":
                        cod.append(i["AmazonOrderId"])
                    else:
                        prepaid.append(i["AmazonOrderId"])
        orders = {"cod":cod,"prepaid" : prepaid}
        dbname = "Amazon" ;tablename="Orders" ; db_system = "sqlite"; out_excel_dir = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
        df = sp_api_report_df_generator(report_type=order_report_types["datewise orders data flatfile"],
                                    start_date=iso_8601_timestamp(5),end_date=iso_8601_timestamp(0))
        if df is not None and not df.empty:
            df.to_sql(name=tablename,con=db_connection(dbname=dbname,db_system=db_system),
                        if_exists='replace',index=False)
        
            for type,value in orders.items():
                execution = filter_query_execution(dbname=dbname,db_system=db_system,tablename=tablename,
                                                filter_rows=value)
                shipdate = amzn_next_ship_date()
                sql_to_excel(sql_cursor=execution[0],query_result=execution[1],
                            out_excel_path=out_excel_dir,excel_filename=f"{shipdate[0]}-{type}")
                
                context["path"] = out_excel_dir
# ERRORS ----------------------------------------------------------------------------------------------------------
        else:
            return HttpResponse("Dataframe is empty")
        return render(request,'amazon_reports.html',context)
    except Exception as e:
        better_error_handling(e)

