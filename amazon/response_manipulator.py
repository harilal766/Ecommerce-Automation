from helpers.messages import *
from datetime import datetime,timedelta
from amazon.sp_api_models import *
from amazon.report_types import *
from amazon.response_manipulator import *
import requests
import pandas as pd
from io import StringIO
from helpers.sql_scripts import sql_to_excel
from collections import namedtuple
from amazon.sp_api_utilities import *





def rep_doc_id_generator(report_id):
    retries =0 ; max_retries = 100 ; delay = 2
    while retries <  max_retries:
        R = Reports(); last_status = None
        report = R.getReport(reportId=report_id)
        if report != None:
            last_status = ''
            status = report["processingStatus"]
            if status == "DONE":
                color_text(message=status,color='green')
                return report.get('reportDocumentId')
            if status in ["IN_QUEUE", "IN_PROGRESS"]:
                if status != last_status:
                    color_text(message=status,color='blue')
                    last_status = status
            elif status == "CANCELLED":
                color_text(message=status,color='red')
                break
            else:
                color_text(message=f"Unknown Status : {status}",color='red')
        else:
            color_text(message="Report Error",color='red')
            break
        retries += 1
        time.sleep(delay)
    raise Exception("Report processing did not complete within the maximum retries.")


def sp_api_report_df(report_type,start_date,end_date):
    try:
        instance = Reports()
        report_id = instance.createReport(reportType=report_type,
                                          dataStartTime=start_date,dataEndTime=end_date)
        report_id = report_id.get('reportId')
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
                    color_text(message="Unable to generate report, status code is not 200",color='red')
            else:
                color_text(message="Report document Id failed,",color='red')
        else:
            color_text(message="Report id failed",color='red')
    except Exception as e:
        better_error_handling(e)

def shipment_report_creator():
    """"
    Step 1 - Order API access
        1. Access the order api and access the shipped (scheduled) and pending pickup orders.
        2. append the cod and prepaid orders in to seperate lists.

    Step 2 - Report API Access
        1. Request the report api based on the scheduled orders type,starting from 5 days ago to today.
        2. filter the received df based on required fields.
        3. with the help of a for loop,
            filter the df again based on the previous cod and prepaid lists and convert it to an excel sheet 
            the sheet names need to be dynamic in future.
    """
    # go to api docs and find other order statueses like waiting for pickup
    order_instance = Orders()
    todays_timestamp = iso_8601_timestamp(0); todays_ind_date = iso_8601_timestamp(0).split("T")[0]
    try:
        # since amazon's time limit for daily orders is 11 am , make \\

        # context initialization for Django...
        context = {"path" : None, "status" : None}
        orders_details = order_instance.getOrders(LastUpdatedAfter=from_timestamp(0),
                                OrderStatuses="Shipped",LatestShipDate=amzn_next_ship_date(),
                                EasyShipShipmentStatuses="PendingPickUp")
        space = " "*14
        cod_orders = []; prepaid_orders = []; order_count = 0
        if isinstance(orders_details,list) and len(orders_details) != 0:
            color_text(message=f"Orders scheduled for {todays_ind_date}")
            for i in orders_details:
                if isinstance(i,dict):
                    order_count += 1
                    # order fields
                    order_id = i["AmazonOrderId"]; 
                    purchase_date = i["PurchaseDate"]; ship_date = i["LatestShipDate"]
                    payment_method = i["PaymentMethod"]
                    # verify again to get orders for today only
                    if ship_date.split("T")[0] == todays_ind_date:
                        if payment_method == "COD":
                            cod_orders.append(order_id)
                        else:
                            prepaid_orders.append(order_id)
                        order_info = f"{order_count}.{order_id} : {purchase_date} - {ship_date} - {payment_method} - {todays_ind_date}"
                        print(order_info)
                else:
                    color_text(message=f"Not a dictionary but of type : {type(i)} ",color="red")
            # Generate reports only if there are cod or prepaid orders
            if len(cod_orders) >0 or len(prepaid_orders)>0:
                shipment_report_df = sp_api_report_df(report_type="GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
                                                        start_date=from_timestamp(5),end_date=todays_timestamp)
                # Filtering based on required columns.
                fields = ["amazon_order_id","purchase_date","last_updated_date","order_status","product_name","item_status",
                    "quantity","item_price","item_tax","shipping_price","shipping_tax"]
                column_filtered_df = (shipment_report_df.filter(fields))
                scheduled_df = column_filtered_df # "Pending - Waiting for Pickup"
                # "Pending - Waiting for Pickup"
                # if the output is available, convert it to excel
                color_text(message=f"COD : {cod_orders}\n{"+++++"}\nPrepaid : {prepaid_orders} \n Dataframe : \n {scheduled_df}")
                color_text(message=scheduled_df)
                
                if not scheduled_df.empty :
                    # after that, make a loop to convert to convert cod and prepaid orders to excel sheet
                    types = {"COD" : cod_orders,"Prepaid":prepaid_orders}
                    for type_key,type_value in types.items():
                        type_filtered_orders_df = scheduled_df[scheduled_df['amazon_order_id'].isin(type_value)]
                        print(type_filtered_orders_df)
                        # Excel path should be changed to dynamic for django.
                        excel_path = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
                        excel_name = f"Scheduled for {todays_ind_date} - {type_key}.xlsx"
                        excel_path = os.path.join(excel_path,excel_name)
                        type_filtered_orders_df.to_excel(excel_writer=excel_path,index="False",
                                                         sheet_name=f"Sheet 1")
            
                else:
                    color_text("There are no scheduled orders",color="red")
        else:
            color_text(message=f"No pending schedules for {todays_timestamp.split("t")[0]}",color="red")
    except Exception as e:
        better_error_handling(e)


from helpers.sql_scripts import db_connection,sql_table_CR
from amazon.sp_api_models import *
from amazon.response_manipulator import *
import pandas as pd






# FUNCTIONS FOR DJANGO ---------------------------------------------------------

def amazon_dashboard(response):
    try:
        if response != None:
            summary_dict = {}
            summary_dict["total_orders"] = 0
            for order in response:
                if type(order) == dict:
                    # taking orders count
                    summary_dict["total_orders"] += 1 

                    ship_by_date = (order['LatestShipDate']).split("T")[0]
                    payment_method = order['PaymentMethod']

                    if ship_by_date not in summary_dict.keys():
                        summary_dict[ship_by_date] = {}
                    if payment_method not in summary_dict[ship_by_date]:
                        summary_dict[ship_by_date][payment_method] = 0
                    summary_dict[ship_by_date][payment_method] += 1
            return summary_dict
        else:
            color_text(message=f"Response : {response}, please check",color="red")
            return None
    except Exception as e:
        better_error_handling(e)