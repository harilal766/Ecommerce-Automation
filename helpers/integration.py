from sp_api import Reports
from sp_api.base import Marketplaces,ReportType,ProcessingStatus
import time,requests,csv,json





credentials = dict(
    refresh_token = "",
    lwa_app_id = "",
    lwa_client_secret = ""
)

marketplace = Marketplaces.US

def getOrders():
    report_type = ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL
    res = Reports(credentials=credentials,marketplace=marketplace)
    data = res.create_report(reportType=report_type,dataStartTime="2021-01-29")
    print(data)
    time.sleep(1000)
