from helpers.messages import color_print
from helpers.messages import better_error_handling
from datetime import datetime
def next_shipment_summary(response):
    try:# only for amazon api, these api contains the field -> AmazonOrderId.
        out_list = response['payload']['Orders']
        today_string = str(datetime.today()).split(" ")[0]
        cod_orders = []; prepaid_orders = []
        order_count = 0; cod_count = 0; prepaid_count = 0
        for item in out_list:
            ship_date_string = str(item['EarliestShipDate']).split("T")[0]
            #ship_date_string = today_string
            last_update_date_string = str(item[ "LastUpdateDate"]).split("T")[0]
            print(f"Ship date : {ship_date_string},  Today : {today_string} :- {ship_date_string == today_string}")
            if (type(item) == dict):
                order_count += 1
                color_print(message=f"Order : {order_count}{'-'*40}",color='blue')
                for key,value in item.items():
                    if  today_string == ship_date_string: 
                        if item['PaymentMethodDetails'] == ['CashOnDelivery']:
                            cod_orders.append(item['AmazonOrderId'])
                        elif item['PaymentMethodDetails'] == ['Standard']:
                            prepaid_orders.append(item['AmazonOrderId'])
                        print(f"{key} : {value}")
                    
        color_print(message=f"COD : {cod_orders} \n Prepaid : {prepaid_orders}",color='blue')
    except Exception as e:
        better_error_handling(e)
        
    color_print(f"Total orders: {order_count}\nCOD for {today_string} : {len(cod_orders)}\nPrepaid for {today_string} : {len(prepaid_orders)}",color='blue')
