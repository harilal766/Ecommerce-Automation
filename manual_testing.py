from amazon.api_models import *
from amazon.report_types import *




R = Reports(); O=Orders()
#rep_id = ins.createReport(reportType=order_report_types["datewise orders data flatfile"])

created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()

# do = R.cancelReport(reportId="")





from amazon.response_manipulator import *
import requests,time
import pandas as pd
type = order_report_types["datewise orders data flatfile"]
# SUCCESS
gsr = R.getReportSchedules(reportTypes=type)
#print(gsr)

def rep_doc_id_generator(report_id):
    while True:
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



def report_generator(report_type):
    start_date = n_days_back_timestamp(7); end_date = n_days_back_timestamp(0)
    try:
        instance = Reports()
        report_id = instance.createReport(reportType=report_type,
                                          dataStartTime=start_date,dataEndTime=end_date)
        report_id = report_id['reportId']

        if report_id:
            color_text(message=f"Report Id Created : {report_id}")
        else:
            color_text(message="Report id failed",color='red')
        
        # Report document id generation.
        rep_doc_id = rep_doc_id_generator(report_id=report_id)
        if rep_doc_id != None:
            color_text(message=f"Report document Id generated : {rep_doc_id}")
            report_document = instance.getReportDocument(reportDocumentId=rep_doc_id)
            # Getting the document url.
            document_url = report_document['url']
            #color_print(message=f"Suspect : {document_url}")
            # Document response.
            document_response = requests.get(document_url)
            print(f"Status code - {document_response.status_code}")

            if document_response.status_code == 200:
                file_content = [[document_response.content]]
                #print(file_content)\

                for line in str(file_content).split("\n"):
                    print(line)
                    print("+++++++++")

                # Writing the data into a flat file
                filepath = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
                filename="^^^^^.tsv"

                filepath = os.path.join(filepath,filename)

                df = pd.DataFrame(file_content)
                df.to_csv(filepath,sep="\t",index=False)
                
            else:
                color_text(message="Unable to generate report.",color='red')

        else:
            color_text(message="Report document Id failed,",color='red')

    except Exception as e:
        better_error_handling(e)


processing_statuses = ["IN_QUEUE","CANCELLED"]

report_generator(report_type=type)

