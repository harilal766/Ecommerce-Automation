from helpers.messages import color_print
from helpers.messages import better_error_handling
from datetime import datetime
def next_shipment_summary(response):
    try:# only for amazon api, these api contains the field -> AmazonOrderId.
        out_list = response['payload']['Orders']
        today_string = str(datetime.today()).split(" ")[0]
        cod_set = set(); prepaid_set = set()
        order_count = 0; cod_count = 0; prepaid_count = 0
        for item in out_list:
            ship_date_string = str(item['EarliestShipDate']).split("T")[0]
            last_update_date_string = str(item[ "LastUpdateDate"]).split("T")[0]
            print(f"Ship date : {ship_date_string},  Today : {today_string}")
            if (type(item) == dict):
                order_count += 1
                color_print(message=f"Order : {order_count}{'-'*40}",color='blue')
                for key,value in item.items():
                    if  ship_date_string == today_string == last_update_date_string and item['PaymentMethodDetails'] == ['CashOnDelivery']:
                        cod_set.add(item['AmazonOrderId'])
                    elif item['PaymentMethodDetails'] == ['Standard'] and ship_date_string == today_string == last_update_date_string:
                        prepaid_set.add(item['AmazonOrderId'])
                    if ship_date_string == today_string:
                        print(f"{key} : {value}")
        color_print(message=f"COD : {cod_set} \n Prepaid : {prepaid_set}",color='blue')
    except Exception as e:
        better_error_handling(e)
        
    color_print(f"Total orders: {order_count}\nCOD for {today_string} : {len(cod_set)}\nPrepaid for {today_string} : {len(prepaid_set)}",color='blue')
