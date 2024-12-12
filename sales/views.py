from django.shortcuts import render
from amazon.response_manipulator import amazon_dashboard
from amazon.sp_api_models import Orders,Reports
from datetime import datetime,timedelta
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *
from helpers.sql_scripts import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
            context["ship_date"] = iso_8601_timestamp(0).split("T")[0]
        else:
            color_text(message="Empty response from getOrders",color="red")
        return render(request,'home.html',context)
    except Exception as e:
        better_error_handling(e)


def amazon_shipment_report(request):
    """"
    Step 1 - Order API access
        1. Access the order api and access the shipped (scheduled) and pending pickup orders.
        2. append the cod and prepaid orders in to seperate lists.

    Step 2 - Report API Access
        1. Request the report api based on the scheduled orders type,starting from 5 days ago to today.
        2. filter the received df based on required fields.
        3. with the help of a for loop,
            filter the df again based on the previous cod and prepaid lists and convert it to an excel sheet 
            the sheet names need to be dynamic in future.
    """
    context = {"path" : None, "status":None }
    # go to api docs and find other order statueses like waiting for pickup
    order_instance = Orders()
    todays_timestamp = iso_8601_timestamp(0); todays_ind_date = iso_8601_timestamp(0).split("T")[0]
    try:
        # since amazon's time limit for daily orders is 11 am , make \\
        # context initialization for Django...
        context = {"path" : None}
        orders_details = order_instance.getOrders(LastUpdatedAfter=from_timestamp(0),
                                OrderStatuses="Shipped",LatestShipDate=amzn_next_ship_date(),
                                EasyShipShipmentStatuses="PendingPickUp")
        space = " "*14
        cod_orders = []; prepaid_orders = []; order_count = 0
        if isinstance(orders_details,list) and len(orders_details) != 0:
            color_text(message=f"Orders scheduled for {todays_ind_date}")
            for i in orders_details:
                if isinstance(i,dict):
                    order_count += 1
                    # order fields
                    order_id = i["AmazonOrderId"]; 
                    purchase_date = i["PurchaseDate"]; ship_date = i["LatestShipDate"]
                    payment_method = i["PaymentMethod"]
                    # verify again to get orders for today only
                    if ship_date.split("T")[0] == todays_ind_date:
                        if payment_method == "COD":
                            cod_orders.append(order_id)
                        else:
                            prepaid_orders.append(order_id)
                        order_info = f"{order_count}.{order_id} : {purchase_date} - {ship_date} - {payment_method} - {todays_ind_date}"
                        print(order_info)
                else:
                    color_text(message=f"Not a dictionary but of type : {type(i)} ",color="red")
            # Generate reports only if there are cod or prepaid orders
            if len(cod_orders) >0 or len(prepaid_orders)>0:
                shipment_report_df = sp_api_report_df(report_type="GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
                                                        start_date=from_timestamp(5),end_date=todays_timestamp)
                # Filtering based on required columns.
                fields = ["amazon_order_id","purchase_date","last_updated_date","order_status","product_name","item_status",
                    "quantity","item_price","item_tax","shipping_price","shipping_tax"]
                column_filtered_df = (shipment_report_df.filter(fields))
                scheduled_df = column_filtered_df # "Pending - Waiting for Pickup"
                # "Pending - Waiting for Pickup"
                # if the output is available, convert it to excel
                color_text(message=f"COD : {cod_orders}\n{"+++++"}\nPrepaid : {prepaid_orders} \n Dataframe : \n {scheduled_df}")
                color_text(message=scheduled_df)
                
                if not scheduled_df.empty :
                    # after that, make a loop to convert to convert cod and prepaid orders to excel sheet
                    types = {"COD" : cod_orders,"Prepaid":prepaid_orders}
                    for type_key,type_value in types.items():
                        type_filtered_orders_df = scheduled_df[scheduled_df['amazon_order_id'].isin(type_value)]
                        print(type_filtered_orders_df)
                        # Excel path should be changed to dynamic for django.
                        excel_path = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
                        excel_name = f"Scheduled for {todays_ind_date} - {type_key}.xlsx"
                        excel_path = os.path.join(excel_path,excel_name)
                        type_filtered_orders_df.to_excel(excel_writer=excel_path,index="False",
                                                         sheet_name=f"Sheet 1")
                        context["path"] = excel_path
                    
                else:
                    color_text("There are no scheduled orders",color="red")
        else:
            color_text(message=f"No pending schedules for {todays_timestamp.split("t")[0]}",color="red")

        return render(request,"amazon_reports.html",context)
    except Exception as e:
        better_error_handling(e)