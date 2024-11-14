from helpers.messages import status_message
from helpers.messages import better_error_handling

def next_shipment_details(response):
    try:# only for amazon api, these api contains the field -> AmazonOrderId.
        out_list = response['payload']['Orders']
        order_count = 0; cod_count = 0; prepaid_count = 0
        for item in out_list:
            if (type(item) == dict):
                order_count += 1
                #status_message(message=f"Order : {order_count}{'-'*40}",color='blue')
                for key,value in item.items():
                    if  key == 'PaymentMethodDetails' and value == ['CashOnDelivery']:
                        cod_count+=1
                    elif key == 'PaymentMethodDetails' and value == ['Standard']:
                        prepaid_count+=1
                    #print(f"{key} : {value}")
    except Exception as e:
        better_error_handling(e)
        
    status_message(f"Total orders: {order_count}, COD : {cod_count}, Prepaid : {prepaid_count}.",color='blue')
