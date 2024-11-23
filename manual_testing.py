from amazon.response_manipulator import n_days_back_timestamp,sp_api_report_generator
from helpers.file_ops import *
from amazon.report_types import *


file_dir = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
filename=f"16 - 23.csv"

print(n_days_back_timestamp(7))


sp_api_report_generator(report_type=order_report_types["datewise orders data flatfile"],
                        start_date=n_days_back_timestamp(7),end_date=n_days_back_timestamp(0),
                        file_dir=file_dir,filename=filename)

