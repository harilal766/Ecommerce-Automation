from helpers.messages import color_print
from helpers.messages import better_error_handling
from datetime import datetime,timedelta
def next_shipment_summary(response):
    try:# only for amazon api, these api contains the field -> AmazonOrderId.
        #out_list = response['payload']['Orders']
        next_shipment_date = ''
        today_string = str(datetime.today()).split(" ")[0]
        cod_orders = []; prepaid_orders = []
        # Counter Initialization
        order_count = 0; cod_count = 0; prepaid_count = 0; field_count = 0
        for item in response:
            #print(item); color_print(message=f"{'-'*80}",color='green')
            ship_date_string = str(item['EarliestShipDate']).split("T")[0]
            #ship_date_string = today_string
            last_update_date_string = str(item["LastUpdateDate"]).split("T")[0]
            #print(f"Ship date : {ship_date_string},  Today : {today_string} :- {ship_date_string == today_string}")
            order_id = item['AmazonOrderId']
            order_count += 1
            #color_print(message=f"Order : {order_count}{'-'*40}",color='blue')
            if type(item) == dict:
                if  today_string == ship_date_string: 
                    field_count+=1
                    if item['PaymentMethodDetails'] == ['CashOnDelivery']:
                        cod_orders.append(order_id)
                    elif item['PaymentMethodDetails'] == ['Standard']:
                        prepaid_orders.append(order_id)
                print(f"{order_count}. {item['AmazonOrderId']}, Ship by date : {ship_date_string}")
                
        boundary = " "   
        id_and_date = f"COD :{cod_orders}\n{boundary}\nPrepaid :{prepaid_orders}\n{boundary}"
        color_print(message=id_and_date,color='blue')
        
    except Exception as e:
        better_error_handling(e)
    color_print(f"Total orders: {order_count}\nCOD for {today_string} : {len(cod_orders)}\nPrepaid for {today_string} : {len(prepaid_orders)}",color='blue')

def report_display(response):
    if len(response) == 0:
        color_print(message=f"Empty Output. : {response}",color='red')
    else:
        for i in response:
            for key,value in i.items():
                    print(f"{key} -:- {value}")
            color_print("------------",color="blue")

def requested_reports(response,report_id = None):
    color = 'blue'
    for report in response:
        if type(report) == dict:
            for key,value in report.items():
                if report['reportId'] == report_id:
                    color_print(message="Target id found.")
                    color = 'green'
                color_print(message = f"{key} - {value}",color=color)
            color_print(message="----------",color='blue')




def n_days_back_timestamp(days):
    try:
        if type(days) == int: 
            # Substract (time now - time n days back) and return the answer in iso format
            return (datetime.utcnow() - timedelta(days=days)).isoformat()
        else:
            color_print(message="Enter a number.",color='red')
    except Exception as e:
        better_error_handling(e)