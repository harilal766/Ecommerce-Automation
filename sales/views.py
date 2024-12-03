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
        dbname = "Amazon" ; tablename="Orders" ; db_system = "sqlite"; out_excel_dir = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
        report_response_df = sp_api_report_df_generator(report_type=order_report_types["datewise orders data flatfile"],
                            start_date=iso_8601_timestamp(4),end_date=iso_8601_timestamp(0))
        print(report_response_df) #✔️
        # 2. If the df is not empty, convert the dataframe into an sql table
        if not report_response_df.empty:
            report_response_df.to_sql(name=tablename,con=db_connection(dbname=dbname,db_system=db_system),
            if_exists='replace',index=False)

            # 3. make a list of types needed
            order_types = ["COD","Other"]
            for type in order_types:
                color_text(message=f"Report generation for {type}")
                ord = Orders()
                orders = ord.getOrders(CreatedAfter=iso_8601_timestamp(2),OrderStatuses="Unshipped",
                                    PaymentMethods=type)

                order_ids = []; 
                next_shipping = amzn_next_ship_date().split("T")[0]
                print(next_shipping)
                count = 0
                for order in orders:
                    latest_ship_date = order["LatestShipDate"].split("T")[0]
                    order_id = order["AmazonOrderId"]
                    if latest_ship_date == next_shipping:
                        count += 1 
                        print(f"{count} - {order_id} - {latest_ship_date}")
                        order_ids.append(order_id)
                        color_text(message="+++++++")

                # 4. Execute the filter query
                execution = query_execution(dbname=dbname,db_system=db_system,
                                tablename=tablename,filter_rows=order_ids)
                connection = execution["connection"] ; cursor = execution["cursor"]
                
                # 5. Convert the result into excel file
                color_text(message=f"Result : \n{cursor}")

                filename = f"{next_shipping} - {type}"
                sql_to_excel(sql_cursor=cursor,query_result=cursor.fetchall(),out_excel_path=out_excel_dir,excel_filename=filename)

                context["path"] = out_excel_dir
                
                db_closer(connection=connection,cursor=cursor)
                
        else:
            color_text(message="Empty dataframe",color="red")
        
        # Return the output for the html template
        return render(request,"amazon_reports.html",context)
    except Exception as e:
        better_error_handling(e)