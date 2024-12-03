from helpers.sql_scripts import sql_table_CR
from helpers.file_ops import *
from sales.views import *



"""


report_response_df = sp_api_report_df_generator(report_type=order_report_types["datewise orders data flatfile"],
                            start_date=iso_8601_timestamp(5),end_date=iso_8601_timestamp(0))
print(report_response_df) #✔️

"""


ord = Orders()
rep = ord.getOrders(CreatedAfter=iso_8601_timestamp(2),OrderStatuses="Unshipped")

print(rep)