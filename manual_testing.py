from amazon.api_models import *
from amazon.report_types import *
from amazon.response_manipulator import *
import requests,time,re,csv
import pandas as pd
from io import StringIO
from helpers.sql_scripts import sql_table_creation_or_updation
type = order_report_types["datewise orders data flatfile"]
def rep_doc_id_generator(report_id):
    while True:
        R = Reports()
        report = R.getReport(reportId=report_id)
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

def file_writer(filepath,filename,data):
    extension = filename.split(".")[-1]
    df = pd.DataFrame(data)
    if extension == "csv":
        df.to_csv(path_or_buf=filepath,encoding='utf-8')

def sp_api_report_generator(report_type,start_date,end_date,file_dir,filename):
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
                    file_content = document_response.content
                    decoded_data = file_content.decode("utf-8") # Decoding the response into utf-8
                    # Writing the data into a csv file
                    filepath = os.path.join(file_dir,filename)
                    data_io = StringIO(decoded_data) # converting the decode data into a file simulation
                    df = pd.read_csv(data_io,sep = '\t')
                    df.to_csv(filepath,index=False)
                else:
                    color_text(message="Unable to generate report.",color='red')
            else:
                color_text(message="Report document Id failed,",color='red')
        else:
            color_text(message="Report id failed",color='red')
    except Exception as e:
        better_error_handling(e)




start_date = n_days_back_timestamp(7); end_date = n_days_back_timestamp(0)
file_dir = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
filename=f"{start_date.split("T")[0]} to {end_date.split("T")[0]}.csv"

sp_api_report_generator(report_type=type,
                        start_date=start_date,end_date=end_date,
                        file_dir=file_dir,filename=filename)


start_date = n_days_back_timestamp(7); end_date = n_days_back_timestamp(0)
