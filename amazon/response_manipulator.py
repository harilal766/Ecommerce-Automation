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
    try:
        ship_by_dates = [] ; total_orders =0
        for i in response:
            if type(i) == dict:
                total_orders+=1
                ship_date = i['EarliestShipDate']
                if ship_date not in ship_by_dates:
                    ship_by_dates.append(ship_date)
                
        
        return (total_orders,ship_by_dates)
        
            
    except Exception as e:
        better_error_handling(e)
    



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