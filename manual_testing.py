from amazon.api_models import *
from amazon.report_types import *



ins = Reports()
rep_id = ins.createReport(reportType=order_report_types["datewise orders data flatfile"])

print(rep_id)