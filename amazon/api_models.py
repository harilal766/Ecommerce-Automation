import requests
from datetime import datetime, timedelta, timezone
from helpers.messages import color_print
from helpers.file_ops import *
from amazon.authorization import *
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

    def response_processor(self,endpoint,json_input=None,params=None,payload=None,method=None):
        # make sure the endpoint have a "/" at the begining and does not end with "/"
        if endpoint[0] != '/':
            endpoint = '/'+endpoint
        # Since majority of methods are GET,...
        if method == None:
            color_print(message=f"{method} method.",color='green')
            response = requests.get(self.base_url+endpoint, headers=self.headers,params = params)
        elif method == 'post':
            color_print(message=f"{method} method.",color='green')
            response = requests.post(self.base_url+endpoint, headers=self.headers,json = json_input)

        color_print(message=f"Status code : {response.status_code} \n Response :",color='blue')
        response.raise_for_status()
        response = response.json()

        if payload == None:
            return response
        else :
            return response[payload]


class Orders(SPAPIBase):
    """ 
        Order api function parameters (optional)
        link : https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#getorders

        getOrderAddress, getOrderItems
        getOrderItemsBuyerInfo, updateShipmentStatus, getOrderRegulatedInfo
        updateVerificationStatus, confirmShipment
    """
    def getOrders(self,CreatedAfter,OrderStatuses):
        endpoint = "/orders/v0/orders"
        self.params.update({
            "CreatedAfter": CreatedAfter,
            "OrderStatuses":OrderStatuses})  
        payload = super().response_processor(endpoint=endpoint,params=self.params,payload='payload')
        return payload.get('Orders')

    def getOrder(self,orderId):
        endpoint = f"/orders/v0/orders/{orderId}"
        self.params.update ({"orderId" : orderId})
        return super().response_processor(endpoint=endpoint,params=self.params,payload='payload')
    
    def getOrderBuyerInfo(self,orderId):
        endpoint = f"/orders/v0/orders/{orderId}/buyerInfo"
        self.params.update ({"orderId" : orderId})
        return super().response_processor(endpoint=endpoint,params=self.params)
    

class Reports(SPAPIBase):
    """
        https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-reference

        cancelReport
        getReportSchedules, createReportSchedule, getReportSchedule, cancelReportSchedule, getReportDocument
    """
    def createReport(self,reportType):
        endpoint = '/reports/2021-06-30/reports'
        data = {
            "reportType":reportType,
            "marketplaceIds" : [self.marketplace_id]
        }
        return super().response_processor(method='post',endpoint=endpoint,json_input=data)
    
    def getReports(self,reportTypes=None,processingStatuses=None):
        endpoint = "/reports/2021-06-30/reports"
        self.params.update({
            "reportTypes" : reportTypes
            })
        return super().response_processor(endpoint=endpoint,params=self.params,payload='reports')
    
    def getReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
        return super().response_processor(endpoint=endpoint,params=self.params)

    def cancelReport():
        pass



