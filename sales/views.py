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
        # 1. Generating the dataframe from sp api reports response
        dbname = "Amazon" ;tablename="Orders" ; db_system = "sqlite"; out_excel_dir = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
        df = sp_api_report_df_generator(report_type=order_report_types["datewise orders data flatfile"],
                            start_date=iso_8601_timestamp(5),end_date=iso_8601_timestamp(0))
        
        # 2. If the df is not empty, convert the dataframe into an sql table
        if df is not None and not df.empty:
            df.to_sql(name=tablename,con=db_connection(dbname=dbname,db_system=db_system),
            if_exists='replace',index=False)

            # 3. Access the order api
            orders_instance = Orders()
            orders = orders_instance.getOrders(CreatedAfter=iso_8601_timestamp(4),LatestShipDate=amzn_next_ship_date(),
                                        OrderStatuses="Unshipped")
            
            # 4. Filter cod and prepaid orders ids form the api
            cod_list = [] ; prepaid_list = []; 
            for i in orders:
                next_ship_date = str(amzn_next_ship_date()).split("T")[0]
                latest_ship_date = i['LatestShipDate'].split("T")[0]
                color_text(message=f"next : {next_ship_date} - latest : {latest_ship_date}",color="red")
                if isinstance(i,dict):
                    if next_ship_date == latest_ship_date:
                        #print(f"{i["AmazonOrderId"]} - {i['LatestShipDate']}")
                        if i["PaymentMethod"] == "COD":
                            cod_list.append(i["AmazonOrderId"])
                        else:
                            prepaid_list.append(i["AmazonOrderId"])
                    else:
                        color_text(message="Shippings for todays date didnt found.",color="red")
                        break

            # 5. Add the cod and prepaid lists into the orders dictionary
            if len(cod_list) > 0 or len(prepaid_list) > 0 :
                shipment_summary_dict = {"cod":cod_list,"prepaid" : prepaid_list}

                # 6. Loop the dict and execute sql table filtering script. 
                for type,value in shipment_summary_dict.items():
                        execution = filter_query_execution(dbname=dbname,db_system=db_system,tablename=tablename,
                                                                    filter_rows=value)
                        shipdate = amzn_next_ship_date()

                        # 7. Convert the sql output into excel sheet.
                        sql_to_excel(sql_cursor=execution[0],query_result=execution[1],
                                    out_excel_path=out_excel_dir,excel_filename=f"{shipdate[0]}-{type}")
                        context["path"] = out_excel_dir
# ERRORS ------------------------------------------------------------------------------------------------------
            else:
                color_text(message="Order ids are empty",color="Red")
        else:
            color_text(message="Empty dataframe",color="red")
        
        # Return the output for the html template
        return render(request,'amazon_reports.html',context)
    except Exception as e:
        better_error_handling(e)

