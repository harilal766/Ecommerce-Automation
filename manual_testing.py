from amazon.api_models import *
from amazon.report_types import *



R = Reports(); O=Orders()
#rep_id = ins.createReport(reportType=order_report_types["datewise orders data flatfile"])

created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()

go = O.getOrders(CreatedAfter=created_after,OrderStatuses='Unshipped')


print(go)