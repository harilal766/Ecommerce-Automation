from amazon.api_models import *
from amazon.report_types import *

"""

R = Reports(); O=Orders()
#rep_id = ins.createReport(reportType=order_report_types["datewise orders data flatfile"])

created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()

# do = R.cancelReport(reportId="")

"""





from helpers.sql_scripts import sql_table_creation_or_updation

win_shopify_fulfilled = r"D:\3.Shopify\fulfilled report"

sql_table_creation_or_updation(dbname="Shopify",tablename="sh_orders",replace_or_append="append",input_file_dir=win_shopify_fulfilled)

