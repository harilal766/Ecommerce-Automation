from amazon.api_models import *
from amazon.report_types import *




R = Reports(); O=Orders()
#rep_id = ins.createReport(reportType=order_report_types["datewise orders data flatfile"])

created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()

# do = R.cancelReport(reportId="")





from amazon.response_manipulator import *
type = order_report_types["datewise orders data flatfile"]
# SUCCESS
gsr = R.getReportSchedules(reportTypes=type)
#print(gsr)


def rep_doc_id_generator(report_id):
    while True:
        report = R.getReport(reportId=report_id)
        status = report["processingStatus"]
        if status == "IN_QUEUE":
            color='blue'
        elif status == "CANCELLED":
            color='red'
        else:
            color='green'
        
        if status == "DONE":
            color_print(message=report['reportDocumentId'],color=color)
            return report['reportDocumentId']
        else:
            color_print(message=status,color=color)
        
        


def report_generator(report_type):
    try:
        instance = Reports()
        report_id = instance.createReport(reportType=report_type,
                                          dataStartTime=n_days_back_timestamp(7),
                                          dataEndTime=n_days_back_timestamp(0))
        report_id = report_id['reportId']
        if report_id:
            color_print(message=f"Report Id Created : {report_id}",color="green")
        
        # Report document id generation.
        rep_doc_id = rep_doc_id_generator(report_id=report_id)
        print(rep_doc_id)

        # amzn1.spdoc.1.4.eu.55c345bc-98a5-433b-874d-a21c8c5db836.T3OZDJHVCBY4M9.2409
        
        #requested_reports(response=status)
    except Exception as e:
        better_error_handling(e)


processing_statuses = ["IN_QUEUE","CANCELLED"]

report_generator(report_type=type)





