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
        ord_ins = Orders(); created_after = (datetime.utcnow() - timedelta(days=4)).isoformat()
        ord_resp = ord_ins.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")
        if ord_resp != None:
            summary = amazon_dashboard(response=ord_resp)
            context = {'shipment_summary' : summary, "ship_date":amzn_next_ship_date().split("T")[0]}
            return render(request,'home.html',context)
        else:
            color_text(message="Empty response from getOrders",color="red")
    except Exception as e:
        better_error_handling(e)

def amazon_reports(request):
    try:
        R = Reports(); O = Orders()
        orders = O.getOrders(CreatedAfter=iso_8601_timestamp(4),LatestShipDate=amzn_next_ship_date(),
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
                sql_to_excel(sql_cursor=execution[0],query_result=execution[1],
                            out_excel_path=out_excel_dir,excel_filename=f"{amzn_next_ship_date()}-{type}")
                
                context = {"path" : out_excel_dir}
            return render(request,'amazon_reports.html',context)
# ERRORS ----------------------------------------------------------------------------------------------------------
        else:
            return HttpResponse("Dataframe is empty")
    except Exception as e:
        better_error_handling(e)

