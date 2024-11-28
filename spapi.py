from amazon.authorization import *
from amazon.api_models import *
from amazon.response_manipulator import *

# item['PaymentMethodDetails']   ['CashOnDelivery']  ['Standard']

ord_ins = Orders()
ord_resp = ord_ins.getOrders(CreatedAfter=iso_8601_timestamp(5),OrderStatuses="Unshipped",
                             EarliestShipDate=iso_8601_timestamp(0))




def amazon_dashboard(response):
    try:
        ship_by_dates = [] ; total_orders =0 ; 
        summary_dict = {} ; sub_dict = {}
        for order in response:
            if type(order) == dict:
                total_orders+=1
                ship_by_date = (order['LatestShipDate']).split("T")[0]
                if ship_by_date not in summary_dict.keys():
                    summary_dict[ship_by_date] = 1
                else:
                    summary_dict[ship_by_date] += 1
        print(summary_dict)
        return (total_orders,summary_dict)
    except Exception as e:
        better_error_handling(e)

amazon_dashboard(response=ord_resp)


