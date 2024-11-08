from datetime import datetime, timedelta, timezone
from amazon.order_table_updater import Orders,Reports
import requests,json
from helpers.messages import better_error_handling,status_message,success_status_msg
from helpers.regex_patterns import amazon_order_id_pattern
from helpers.file_ops import text_input_checker
created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()


        
def amazon_api_driver(option):
    orders_instance=Orders() ; reports_instance = Reports()
    try:
        if "orders" in option:
            orders = orders_instance.getOrders(created_after,order_status="Unshipped")
            data = json.dumps(orders,indent=4)
            print(orders)
        elif not "orders" in option and "order" in option:
            order = orders_instance.getOrder(orderId=
                                             text_input_checker(display_message="Enter the order id : ",
                                                                input_pattern=amazon_order_id_pattern))
            print(order)



    except Exception as e:
        better_error_handling(e)
    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", err)



