from datetime import datetime,timedelta
from helpers.messages import *
from amazon.sp_api_models import *


# SP API Utilities needed for several needs
today = datetime.today()

today_start_time = today.replace(hour=0,minute=0,second=0,microsecond=0).isoformat()+"Z"
today_end_time = today.replace(hour=23,minute=59,second=59,microsecond=99999).isoformat()+"Z"

def iso_8601_timestamp(days):
    try:
        if type(days) == int: 
            # Substract (time now - time n days back) and return the answer in iso format
            return (datetime.utcnow() - timedelta(days=days)).isoformat()
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
    

