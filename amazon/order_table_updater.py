import requests
from datetime import datetime, timedelta, timezone
from helpers.messages import color_print
from helpers.file_ops import *
from amazon.authorization import get_or_generate_access_token
created_after = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()


class SPAPIBase:
    def __init__(self,base_url="https://sellingpartnerapi-eu.amazon.com",marketplace_id="A21TJRUUN4KGV"):
        self.access_token = get_or_generate_access_token()
        self.base_url = base_url
        self.marketplace_id = marketplace_id
        self.headers = {
            "x-amz-access-token": self.access_token,
            "Content-Type": "application/json"
            }
        # Common parameters, individual ones will be added from the respective functions
        self.params = {
            "MarketplaceIds": self.marketplace_id,
        }

class Orders(SPAPIBase):
    """ 
        Order api function parameters (optional)
        link : https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#getorders

        getOrders, getOrder, getOrderBuyerInfo, getOrderAddress, getOrderItems
        getOrderItemsBuyerInfo, updateShipmentStatus, getOrderRegulatedInfo
        updateVerificationStatus, confirmShipment
    """
    def getOrders(self,CreatedAfter,OrderStatuses):
        self.params.update({
            "CreatedAfter": CreatedAfter,
            "OrderStatuses":OrderStatuses
        })
        endpoint = "/orders/v0/orders" 
        
        response = requests.get(self.base_url+endpoint, headers=self.headers, params=self.params)
        response.raise_for_status()
        response = response.json()
        orders = response['payload']['Orders']
        return orders

    def getOrder(self,orderId):
        """
        Rate (requests per second)	Burst
                            0.5	    30
        """
        endpoint = f"/orders/v0/orders/{orderId}"
        self.params.update ({
            "orderId" : orderId
        })
        response = requests.get(self.base_url+endpoint, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()
    
    def getOrderBuyerInfo(self,orderId):
        """
        Rate (requests per second)	Burst
                            0.5	    30
        """
        endpoint = f"/orders/v0/orders/{orderId}/buyerInfo"
        self.params.update ({
            "orderId" : orderId
        })
        response = requests.get(self.base_url+endpoint, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()

    

class Reports(SPAPIBase):
    """
        https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-reference

        getReports, createReport, getReport, cancelReport
        getReportSchedules, createReportSchedule, getReportSchedule, cancelReportSchedule, getReportDocument
    """
    # Add getReports() here
    """
    Order Report Types
    "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL"
        GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_SHIPPING
        GET_ORDER_REPORT_DATA_INVOICING
        GET_ORDER_REPORT_DATA_TAX
        GET_ORDER_REPORT_DATA_SHIPPING
        GET_FLAT_FILE_ORDER_REPORT_DATA_INVOICING
        GET_FLAT_FILE_ORDER_REPORT_DATA_SHIPPING
        GET_FLAT_FILE_ORDER_REPORT_DATA_TAX
        GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL
        GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL
        GET_FLAT_FILE_ARCHIVED_ORDERS_DATA_BY_ORDER_DATE
        GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL
        GET_XML_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL
        GET_FLAT_FILE_PENDING_ORDERS_DATA
        GET_PENDING_ORDERS_DATA
        GET_CONVERGED_FLAT_FILE_PENDING_ORDERS_DATA
   
    Return Report Types
        GET_XML_RETURNS_DATA_BY_RETURN_DATE
        GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE
        GET_XML_MFN_PRIME_RETURNS_REPORT
        GET_CSV_MFN_PRIME_RETURNS_REPORT
        GET_XML_MFN_SKU_RETURN_ATTRIBUTES_REPORT
        GET_FLAT_FILE_MFN_SKU_RETURN_ATTRIBUTES_REPORT
    """
    
    def createReport(self,reportType):
        endpoint = '/reports/2021-06-30/reports'
        data = {
            "reportType":reportType,
            "marketplaceIds" : [self.marketplace_id]
        }
        # {'reportId': '50446020045'}
        response = requests.post(self.base_url+endpoint,headers=self.headers, json=data)
        color_print(message=f"Status code : {response.status_code}",color='blue')
        color_print(message="Response :\n",color='blue')
        #response.raise_for_status()
        return response.json()
    
    def getReports():
        pass



