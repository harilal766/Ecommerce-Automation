from amazon.api_models import *
from amazon.report_types import *




R = Reports(); O=Orders()
#rep_id = ins.createReport(reportType=order_report_types["datewise orders data flatfile"])

created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()

# do = R.cancelReport(reportId="")





from amazon.response_manipulator import *
import requests,time
type = order_report_types["datewise orders data flatfile"]
# SUCCESS
gsr = R.getReportSchedules(reportTypes=type)
#print(gsr)

def rep_doc_id_generator(report_id):
    while True:
        report = R.getReport(reportId=report_id)
        status = report["processingStatus"]
        if status == "DONE":
            color_print(message=report['reportDocumentId'],color='green')
            return report['reportDocumentId']
        if status == "IN_QUEUE":
            color_print(message=status,color='blue')
        elif status == "CANCELLED":
            color_print(message=status,color='red')
        else:
            color_print(message=status,color='green')

def report_generator(report_type):
    try:
        instance = Reports()
        report_id = instance.createReport(reportType=report_type,
                                          dataStartTime=n_days_back_timestamp(7),
                                          dataEndTime=n_days_back_timestamp(0))
        report_id = report_id['reportId']

        if report_id:
            color_print(message=f"Report Id Created : {report_id}")
        else:
            color_print(message="Report id failed",color='red')
        
        # Report document id generation.
        rep_doc_id = rep_doc_id_generator(report_id=report_id)
        if rep_doc_id != None:
            color_print(message=f"Report document Id generated : {rep_doc_id}")
            report_document = instance.getReportDocument(reportDocumentId=rep_doc_id)
            # Getting the document url.
            document_url = report_document['url']
            #color_print(message=f"Suspect : {document_url}")
            # Document response.
            document_response = requests.get(document_url)
            print(f"Status code - {document_response.status_code}")

            if document_response.status_code == 200:
                print(document_response.content)

        else:
            color_print(message="Report doucment Id failed,",color='red')

        

    except Exception as e:
        better_error_handling(e)


processing_statuses = ["IN_QUEUE","CANCELLED"]

report_generator(report_type=type)

