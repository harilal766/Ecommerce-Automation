from datetime import datetime, timedelta, timezone
from amazon.order_table_updater import SPAPIBase,Orders,Reports
import requests,json
from helpers.messages import better_error_handling,status_message,success_status_msg
from helpers.regex_patterns import amazon_order_id_pattern
from helpers.file_ops import text_input_checker
created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()

        
def amazon_api_driver(option):
    try:
        if "orders" in option:
            instance = Orders()
            response = instance.getOrders(created_after,order_status="Unshipped")
        elif not "orders" in option and "order" in option:
            instance = Orders()
            response = instance.getOrder(orderId=
                                             text_input_checker(display_message="Enter the order id : ",
                                                                input_pattern=amazon_order_id_pattern))
        elif "Amazon report" in option:
            instance = Reports()
            response = instance.getReports()
        data = json.dumps(response,indent=4)
        print(response)



    except Exception as e:
        better_error_handling(e)
    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", err)



