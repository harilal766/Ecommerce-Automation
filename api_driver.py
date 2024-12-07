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
    try:
        orders_details = order_instance.getOrders(CreatedAfter=from_timestamp(1),
                                                        OrderStatuses="Unshipped")
        space = " "*14
        if orders_details != None:
            color_text(message="Order id"+space+"Purchase date"+space+"Ship date"+space+"Payment method",color="blue",bold=True)
            for i in orders_details:
                if isinstance(i,dict):
                    # order fields
                    order_id = i["AmazonOrderId"]; 
                    purchase_date = i["PurchaseDate"]; ship_date = i["LatestShipDate"]
                    payment_method = i["PaymentMethod"]

                    order_info = f"{order_id} : {purchase_date} - {ship_date} - {payment_method}"

                    print(order_info)
                    
                else:
                    color_text(message="EMPTY",color="red")

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




