from datetime import datetime, timedelta, timezone
from amazon.sp_api_models import SPAPIBase,Orders,Reports
from amazon.response_manipulator import *
import requests,json
from helpers.messages import better_error_handling,color_text,success_status_msg
from helpers.regex_patterns import amazon_order_id_pattern
from helpers.file_ops import *
from amazon.report_types import *
from amazon.sp_api_utilities import *
def response_checker(response):
    if not response == None:
        return response
    else:
        return None
        color_text(message="Empty response from api driver.",color="red")

"""
Scheduled orders are not available via Unshipped
"""





order_instance = Orders()

# One function to get order details
def orders_fetcher():
    # go to api docs and find other order statueses like waiting for pickup
    order_instance = Orders()
    todays_timestamp = iso_8601_timestamp(0); todays_ind_date = iso_8601_timestamp(0).split("T")[0]
    try:
        # since amazon's time limit for daily orders is 11 am , make \\

        # context initialization for Django...
        context = {"path" : None, "status" : None}
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
                        
                        type_filtered_orders_df.to_excel(excel_writer=os.path.join(excel_path,excel_name),index="False",
                                                         sheet_name=f"Sheet 1")
                else:
                    color_text("There are no scheduled orders",color="red")
                    
        else:
            color_text(message=f"No pending schedules for {todays_timestamp.split("t")[0]}",color="red")
    except Exception as e:
        better_error_handling(e)


def api_driver(option):
    try:
        # Assigining the instance and response based on the selection.
        if 'amazon' in option:
            # For getOrders
            if "orders" in option:
                summary = orders_fetcher()
                print(summary)
                
                
            # For a single order details
            elif not "orders" in option and "order" in option:
                response = order_instance.getOrder(orderId=
                                                text_input_checker(display_message="Enter the order id : ",
                                                                    input_pattern=amazon_order_id_pattern))
            elif "buyer info" in option:
                response = order_instance.getOrderBuyerInfo(orderId=
                                                      text_input_checker(display_message="Enter the order id : ",
                                                                    input_pattern=amazon_order_id_pattern))


    
        # Print the data.
        
        
        
        # find the dict in which orders are found
        
    except Exception as e:
        better_error_handling(e)
    except requests.exceptions.HTTPError as err:
        better_error_handling(err)




