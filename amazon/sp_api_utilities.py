from datetime import datetime,timedelta
from helpers.messages import *
from amazon.sp_api_models import *

from datetime import datetime
from pytz import timezone


# SP API Utilities needed for several needs

def from_timestamp(days):
    date = (datetime.utcnow() - timedelta(days=days))
    today_start_time = date.replace(hour=0,minute=0,second=0,microsecond=0).isoformat()+"Z"
    return today_start_time

def to_timestamp(days):
    date = (datetime.utcnow() - timedelta(days=days))
    today_end_time = date.replace(hour=23,minute=59,second=59,microsecond=99999).isoformat()+"Z"
    return today_end_time

def iso_8601_timestamp(days):
    try:
        if type(days) == int: 
            # Substract (time now - time n days back) and return the answer in iso format
            ind_timestamp = (datetime.now(timezone("Asia/Kolkata"))-timedelta(days=days))
            return ind_timestamp.isoformat()
        else:
            color_text(message="Enter a number.",color='red')
    except Exception as e:
        better_error_handling(e)

# '2024-12-18T18:30:00Z

def amzn_next_ship_date(out=None):
    if datetime.now().time().hour >= 11:
    # if the time is past 11:00 AM and todays scheduling is done, return tomorrows date if not a holiday
        return iso_8601_timestamp(-1)
    else:
        return iso_8601_timestamp(0)
    
import pandas as pd
def manual_report_maker(template_file,template_filepath,
                        product_name_column,input_array,
                        out_filename,out_filepath):
    """
    read an excel sheet and print the contents
    locate the prodcut name and count
    populate it with the input array only if target column is empty.
    """
    try:
        # read data from template excel file only if the file exists..

        input_path = os.listdir(path=template_filepath)
        if template_file in input_path:
            # join the file and filepath
            template_filepath = os.path.join(template_filepath,template_file)
            # read the excel file
            df = pd.read_excel(template_filepath)
            # make changes to the file
            df[product_name_column] = input_array\
            # print for confirmation
            print(df)

            # save to a new file
            df.to_excel(excel_writer=os.path.join(out_filepath,out_filename),
                        index=False)
            # make sure outout is saved 
            out = os.listdir(path=out_filepath)
            if out_filename in out:
                color_text(message=f"Manual report saved to : {out_filepath}")
            else:
                color_text(message="Out excel sheet not saved.",color="red")
        else:
            color_text(message="Input directory does not exist",color="red")
        
    except Exception as e:
        better_error_handling(e)