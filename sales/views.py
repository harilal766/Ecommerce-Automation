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

def amazon_shipment_report(request):
    try: 
        # initializing the context
        context = {"path":None}; cod_list = [] ; prepaid_list = []; 
        # 1. Generating the dataframe from sp api reports response
        dbname = "Amazon" ;tablename="Orders" ; db_system = "sqlite"; out_excel_dir = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
        report_response_df = sp_api_report_df_generator(report_type=order_report_types["datewise orders data flatfile"],
                            start_date=iso_8601_timestamp(4),end_date=iso_8601_timestamp(0))
        print(report_response_df) #✔️
        # 2. If the df is not empty, convert the dataframe into an sql table
        if report_response_df is not None and not report_response_df.empty:
            report_response_df.to_sql(name=tablename,con=db_connection(dbname=dbname,db_system=db_system),
            if_exists='replace',index=False)

            # 3. Access the order api
            orders_instance = Orders()
            orders = orders_instance.getOrders(CreatedAfter=iso_8601_timestamp(4),LatestShipDate=amzn_next_ship_date())
            print(orders[0]["PaymentMethod"])
            # 4. Filter cod and prepaid orders ids form the api
            for order in orders:
                amazon_order_id = order.get("AmazonOrderId",None)
                next_ship_date = str(amzn_next_ship_date()).split("T")[0]
                latest_ship_date = order['LatestShipDate'].split("T")[0]
                last_update_date = order['LastUpdateDate'].split("T")[0]
                today_date = iso_8601_timestamp(0).split("T")[0]
                order_status = order['OrderStatus'] # Pending - Waiting for Pick Up
                payment_method = order.get('PaymentMethod',"N/A")
                color_text(message=f"next : {next_ship_date} - latest : {latest_ship_date}",color="red")
                if isinstance(order,dict):
                    if (next_ship_date == latest_ship_date) and (last_update_date == today_date):
                        color_text(message=f"{amazon_order_id} - {payment_method}",end="-")
                        print(f"{latest_ship_date} & {next_ship_date}") #✔️
                        #print(f"{i["AmazonOrderId"]} - {i['LatestShipDate']}")
                        if payment_method == 'COD':
                            cod_list.append(amazon_order_id)
                        else:
                            prepaid_list.append(amazon_order_id)
            shipment_summary_dict = {"cod":cod_list,"prepaid" : prepaid_list}

            context["path"] = shipment_summary_dict
        else:
            color_text(message="Empty dataframe",color="red")
        
        # Return the output for the html template
        return render(request,"amazon_reports.html",context)
    except Exception as e:
        better_error_handling(e)