from helpers.file_ops import *
import requests
from amazon.authorization import *
from datetime import datetime


from amazon.api_models import Reports



order_report_types = {
    
        "" : "GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_SHIPPING",
        "" : "GET_ORDER_REPORT_DATA_INVOICING",
        "" : "GET_ORDER_REPORT_DATA_TAX",
        "" : "GET_ORDER_REPORT_DATA_SHIPPING",
        "" : "GET_FLAT_FILE_ORDER_REPORT_DATA_INVOICING",
        "" : "GET_FLAT_FILE_ORDER_REPORT_DATA_SHIPPING",
        "" : "GET_FLAT_FILE_ORDER_REPORT_DATA_TAX",
        "" : "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL",
        "" : "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
        "" : "GET_FLAT_FILE_ARCHIVED_ORDERS_DATA_BY_ORDER_DATE",
        "" : "GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL",
        "" : "GET_XML_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
        "" : "GET_FLAT_FILE_PENDING_ORDERS_DATA",
        "" : "GET_PENDING_ORDERS_DATA",
        "" : "GET_CONVERGED_FLAT_FILE_PENDING_ORDERS_DATA",
}
ins = Reports()
type = "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL"
#rep = ins.createReport(reportType=type)



requested_reports = ins.getReports(reportTypes=type)

for i in requested_reports:
    print(i); print("++++++++++")



