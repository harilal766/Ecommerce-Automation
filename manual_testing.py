from amazon.api_models import *
from amazon.report_types import *



R = Reports(); O=Orders()
#rep_id = ins.createReport(reportType=order_report_types["datewise orders data flatfile"])

created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()

# do = R.cancelReport(reportId="")






# SUCCESS
gsr = R.getReportSchedules(reportTypes=order_report_types["datewise orders data flatfile"])
print(gsr)


def report_generator(report_type):
    try:
        instance = Reports()
        report_id = instance.createReport(reportType=report_type)
        if report_id:
            color_print(message=f"Report Id Created : {report_id}",color="green")
        
        # status finder
        status = instance.getReports(reportTypes=report_type)
        color_print(message=f"Status : {status}",color='red')
    except Exception as e:
        better_error_handling(e)

report_generator(report_type=order_report_types["datewise orders data flatfile"])
