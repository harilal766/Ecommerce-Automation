from helpers.messages import *
from datetime import datetime,timedelta
from amazon.api_models import *
from amazon.report_types import *
from amazon.response_manipulator import *
import requests
import pandas as pd
from io import StringIO


from collections import namedtuple
def sp_api_shipment_summary(response):
    try:# only for amazon api, these api contains the field -> AmazonOrderId.
        #out_list = response['payload']['Orders']
        next_shipment_date = ''

        ship_by_date = str(datetime.today()).split(" ")[0]
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
            #color_print(message=f"Order : {order_count}{'-'*40}",color='blue')
            if type(item) == dict:
                if  ship_by_date == ship_date_string: 
                    field_count+=1; order_count += 1
                    if item['PaymentMethodDetails'] == ['CashOnDelivery']:
                        cod_orders.append(order_id)
                    elif item['PaymentMethodDetails'] == ['Standard']:
                        prepaid_orders.append(order_id)
                print(f"{order_count}. {item['AmazonOrderId']}, Ship by date : {ship_date_string}")
        
                
        boundary = " "
        id_and_date = f"COD :{cod_orders}\n{boundary}\nPrepaid :{prepaid_orders}\n{boundary}"
        color_text(message=id_and_date,color='blue')

        orders = namedtuple("Orders",["cod","prepaid","order_count"])
        return orders (cod_orders,prepaid_orders,order_count)
        #return { "cod" :cod_orders, "prepaid" : prepaid_orders}
    
        
    except Exception as e:
        better_error_handling(e)
    color_text(f"Total orders: {order_count}\nCOD for {ship_by_date} : {len(cod_orders)}\nPrepaid for {ship_by_date} : {len(prepaid_orders)}",color='blue')



def n_days_timestamp(days):
    try:
        if type(days) == int: 
            # Substract (time now - time n days back) and return the answer in iso format
            return (datetime.utcnow() - timedelta(days=days)).isoformat()
        else:
            color_text(message="Enter a number.",color='red')
    except Exception as e:
        better_error_handling(e)




def rep_doc_id_generator(report_id):
    while True:
        R = Reports()
        report = R.getReport(reportId=report_id)
        if report != None:
            status = report["processingStatus"]
            if status == "DONE":
                color_text(message=status,color='green')
                return report['reportDocumentId']
            if status == "IN_QUEUE":
                color_text(message=status,color='blue')
            elif status == "CANCELLED":
                color_text(message=status,color='red')
            else:
                color_text(message=status,color='green')
        else:
            color_text(message="Report Error",color='red')
            break


def sp_api_report_df_generator(report_type,start_date,end_date):
    try:
        instance = Reports()
        report_id = instance.createReport(reportType=report_type,
                                          dataStartTime=start_date,dataEndTime=end_date)
        report_id = report_id['reportId']
        if report_id:
            color_text(message=f"Report Id Created : {report_id}")
            # Report document id generation.
            rep_doc_id = rep_doc_id_generator(report_id=report_id)
            if rep_doc_id != None:
                color_text(message=f"Report document Id generated : {rep_doc_id}")
                report_document = instance.getReportDocument(reportDocumentId=rep_doc_id)
                document_url = report_document['url']
                document_response = requests.get(document_url)
                print(f"Status code - {document_response.status_code}")
                if document_response.status_code == 200:
                    byte_string = document_response.content
                    decoded_data = byte_string.decode("utf-8") # Decoding the response into utf-8

                   # Returning the dataframe
                    data_io = StringIO(decoded_data) # converting the decode data into a file simulation
                    df = pd.read_csv(data_io,sep = '\t')

                    new_headers = []
                    if not df.empty:
                        # making sure column have underscore word seperator
                        for column in  df.columns.tolist():
                            underscore = column.replace("-","_")
                            new_headers.append(underscore)

                        df.columns = new_headers
                        return df
                            
                    else : 
                        color_text(message="There was an error in generating the dataframe",color='red')
                else:
                    color_text(message="Unable to generate report.",color='red')
            else:
                color_text(message="Report document Id failed,",color='red')
        else:
            color_text(message="Report id failed",color='red')
    except Exception as e:
        better_error_handling(e)




# FUNCTIONS FOR DJANGO ---------------------------------------------------------

def amazon_dashboard(response):
    try:
        ship_by_dates = [] ; order_dates = {} ;total_orders =0
        for i in response:
            if type(i) == dict:
                total_orders+=1
                ship_date = (i['EarliestShipDate']).split("T")[0]
                if ship_date not in ship_by_dates:
                    ship_by_dates.append(ship_date)
        return (total_orders,ship_by_dates)
        
            
    except Exception as e:
        better_error_handling(e)