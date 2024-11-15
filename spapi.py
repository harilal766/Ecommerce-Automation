import os
from dotenv import load_dotenv

load_dotenv()
# Replace these with your credentials
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

credentials = dict(
    refresh_token=REFRESH_TOKEN,
    lwa_app_id=CLIENT_ID,
    lwa_client_secret=CLIENT_SECRET
)

SP_API_DEFAULT_MARKETPLACE= "IN"

"""
SomeClient(
    marketplace="Marketplaces.IN", *,
    refresh_token=None,
    account='default',
    credentials=None,
    restricted_data_token=None
)
"""

from sp_api.base import Marketplaces
from sp_api.api import Orders

from helpers.messages import better_error_handling

# Order...
order_client = Orders(credentials=credentials, marketplace=Marketplaces.DE)
order = order_client.get_order('403-1082177-4218763')
#print(order) # `order` is an `ApiResponse`
#print(order.payload) # `payload` contains the original response


# Orders
"""
from datetime import datetime, timedelta
from sp_api.base import Marketplaces
from sp_api.api import Orders
from sp_api.util import throttle_retry, load_all_pages

@load_all_pages(next_token_param='next_token')
@throttle_retry()
@load_all_pages()
def load_all_orders(**kwargs):
    
    # generator function to return all pages, obtained by NextToken
    
    return Orders().get_orders(**kwargs)


for page in load_all_orders(LastUpdatedAfter=(datetime.utcnow() - timedelta(days=7)).isoformat()):
    for order in page.payload.get('Orders'):
        print(order)
"""
# Reports....
from datetime import datetime, timedelta
from sp_api.api import ReportsV2
from sp_api.base.reportTypes import ReportType
import os 
from helpers.messages import color_print
os.environ['LWA_APP_ID'] = CLIENT_ID
os.environ['LWA_CLIENT_SECRET'] = CLIENT_SECRET
os.environ['SP_API_REFRESH_TOKEN'] = REFRESH_TOKEN


# Report Creation...
def n_days_back_timestamp(days):
    try:
        if type(days) == int: 
            # Substract (time now - time n days back) and return the answer in iso format
            return (datetime.utcnow() - timedelta(days=days)).isoformat()
        else:
            color_print(message="Enter a number.",color='red')
    except Exception as e:
        better_error_handling(e)
        


n_days_back=n_days_back_timestamp(7)
yesterday=n_days_back_timestamp(1)


res = ReportsV2().create_report(
    reportType=ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL,
    # optionally, you can set a start and end time for your report
    dataStartTime=n_days_back,
    dataEndTime=yesterday
    )
color_print(message=f"Reports From {n_days_back} To {yesterday}",color='blue')
#print(res)
report_id = res.payload['reportId']
color_print(message=f"Report Id : {report_id}",color='green') # object containing a report id
















































"""
from amazon.order_table_updater import Orders
created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()


instance = Orders()
resp = instance.getOrders(CreatedAfter=created_after,OrderStatuses='Unshipped')

print(resp)

"""