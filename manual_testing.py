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


def report_status_checker(report_id):
    while True:
        report = R.getReport(reportId=report_id)
        print(report)
        if report["processingStatus"] == "IN_QUEUE":
            color_print(message="Waiting...",color='blue')
        elif report["processingStatus"] == "CANCELLED":
            color_print(message="Cancelled.",color='red')
            break
        else:
            color_print(message="Success.",color='green')
            break
        
        


def report_generator(report_type):
    try:
        instance = Reports()
        report_id = instance.createReport(reportType=report_type)
        report_id = report_id['reportId']
        if report_id:
            color_print(message=f"Report Id Created : {report_id}",color="green")
        
        # status finder
        status = report_status_checker(report_id=report_id)
        print(status)
        
        #requested_reports(response=status)
    except Exception as e:
        better_error_handling(e)

#report_generator(report_type=order_report_types["datewise orders data flatfile"])

processing_statuses = ["IN_QUEUE","CANCELLED"]
#print(f"{n_days_back_timestamp(7)} to {n_days_back_timestamp(0)}")


#o = R.getReports(reportTypes=type,processingStatuses=processing_statuses[0])

report_generator(report_type=type)





