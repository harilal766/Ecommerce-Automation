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
def start_timestamp(days):
    date = (datetime.utcnow() - timedelta(days=days))
    today_start_time = date.replace(hour=0,minute=0,second=0,microsecond=0).isoformat()+"Z"
    return today_start_time

        
def api_driver(option):
    try:
        # Assigining the instance and response based on the selection.
        if 'amazon' in option:
            instance = Orders()
            # For getOrders
            if "orders" in option:
                # go to api docs and find other order statueses like waiting for pickup
                shipment_details = instance.getOrders(CreatedAfter=start_timestamp(0),
                                                      OrderStatuses="Unshipped")
                verified_response = response_checker(shipment_details)

                space = " "*14
                
                if shipment_details != None:
                    color_text(message="Order id"+space+"Purchase date"+space+"Ship date"+space+"Payment method",color="blue",bold=True)
                    for i in verified_response:
                        if isinstance(i,dict):
                            # order fields
                            order_id = i["AmazonOrderId"]; 
                            purchase_date = i["PurchaseDate"]; ship_date = i["LatestShipDate"]
                            payment_method = i["PaymentMethod"]
                            
                            print(f"{order_id} : {purchase_date} - {ship_date} - {payment_method}")
                else:
                    color_text(message="EMPTY",color="red")
                
            # For a single order details
            elif not "orders" in option and "order" in option:
                response = instance.getOrder(orderId=
                                                text_input_checker(display_message="Enter the order id : ",
                                                                    input_pattern=amazon_order_id_pattern))
            elif "buyer info" in option:
                response = instance.getOrderBuyerInfo(orderId=
                                                      text_input_checker(display_message="Enter the order id : ",
                                                                    input_pattern=amazon_order_id_pattern))


    
        # Print the data.
        
        
        
        # find the dict in which orders are found
        
    except Exception as e:
        better_error_handling(e)
    except requests.exceptions.HTTPError as err:
        better_error_handling(err)




