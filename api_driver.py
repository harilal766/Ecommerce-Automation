from datetime import datetime, timedelta, timezone
from amazon.api_models import SPAPIBase,Orders,Reports
from amazon.response_manipulator import next_shipment_summary,report_display
import requests,json
from helpers.messages import better_error_handling,color_text,success_status_msg
from helpers.regex_patterns import amazon_order_id_pattern
from helpers.file_ops import *
from amazon.report_types import *




created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()

        
def api_driver(option):
    try:
        # Assigining the instance and response based on the selection.
        if 'amazon' in option:
            instance = Orders()
            # For getOrders
            if "orders" in option:
                # go to api docs and find other order statueses like waiting for pickup
                response = instance.getOrders(CreatedAfter=created_after,
                                              OrderStatuses="Unshipped")
                response = next_shipment_summary(response=response)
            # For a single order details
            elif not "orders" in option and "order" in option:
                response = instance.getOrder(orderId=
                                                text_input_checker(display_message="Enter the order id : ",
                                                                    input_pattern=amazon_order_id_pattern))
            elif "buyer info" in option:
                response = instance.getOrderBuyerInfo(orderId=
                                                      text_input_checker(display_message="Enter the order id : ",
                                                                    input_pattern=amazon_order_id_pattern))
            
            elif "report api" in option:
                instance = Reports()
                response = instance.getReports(reportTypes=order_report_types["datewise archived orders data flatfile"])
                response= report_display(response)

        elif "Shopify" in option:
            pass

        
        # Print the data.
        print(response)
        # find the dict in which orders are found
        
    except Exception as e:
        better_error_handling(e)
    except requests.exceptions.HTTPError as err:
        better_error_handling(err)




