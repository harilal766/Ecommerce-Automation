from helpers.sql_scripts import sql_table_CR
from helpers.messages import *
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *


# time is must, if days == 0 , treat time as of todays
# for normal timestamp, there shouldnt be much parameters
# if date is needed only and not time type is not needed.
def timestamp(days,type=None,split=None):
    # types : iso 8601, 
    ind_timestamp = (datetime.now(timezone("Asia/Kolkata"))-timedelta(days=days))
    if type == "iso":
        return ind_timestamp.isoformat()
    elif type == "utc":
        return ind_timestamp.utcnow()
    # if the split is none, return the full time stamp







manual_report_maker(template_file="amazon manual report template.xlsx",
                    template_filepath=dir_switch(win=win_amazon_manual_report,lin=lin_amazon_manual_report),
                    product_name_column="Name of Product",
                    input_array=["a","b"],
                    out_filename=f"Amazon manual report COD.xlsx",
                    out_filepath=dir_switch(win=win_amazon_manual_report_out,lin=lin_amazon_manual_report_out)
                    )    