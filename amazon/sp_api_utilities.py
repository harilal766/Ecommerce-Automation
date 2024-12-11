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



def amzn_next_ship_date(out=None):
    if datetime.now().time().hour >= 11:
    # if the time is past 11:00 AM and todays scheduling is done, return tomorrows date if not a holiday
        return iso_8601_timestamp(-1)
    else:
        return iso_8601_timestamp(0)
    

