import requests
from datetime import datetime, timedelta, timezone
from helpers.messages import color_text
from helpers.file_ops import *
from amazon.authorization import *
import time

created_after = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()


normal_endpoint = "https://sellingpartnerapi-eu.amazon.com"
sandbox_endpoint = "https://sandbox.sellingpartnerapi-eu.amazon.com"

class SPAPIBase:
    def __init__(self,base_url=normal_endpoint,marketplace_id="A21TJRUUN4KGV"):
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
        self.success_codes = {200,201}

    def execute_request(self,endpoint,method,json_input=None,params=None,payload=None,rate_per_second=None,burst=None):
        retry = 5; delay=1
        # set the initial request count as zero,
        try:
            # make sure the endpoint have a "/" at the begining and does not end with "/"
            if endpoint[0] != '/':
                endpoint = '/'+endpoint
                status_end = " | "
                url = self.base_url+endpoint
                # Since majority of methods are GET,...
                if method.lower() == 'get':
                    response = requests.get(url, headers=self.headers,params = params,timeout=10)
                elif method.lower() == 'post':
                    response = requests.post(url, headers=self.headers,json = json_input,timeout=10)
                elif method.lower() == 'delete':
                    response = requests.delete(url, headers=self.headers,timeout=10)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                if response.status_code == 429:
                    time.sleep(delay)
                    delay *=2
                    color_text(message=f"Rate limit reached, retrying in {delay} seconds.",color='red')
                else:
                    response.raise_for_status()
                    response_data = response.json()
                    return response_data.get(payload) if payload else response_data
        except requests.exceptions.RequestException as e:
            better_error_handling(f"Error : {e}")

        """
        for attempt in range(retry):
            
        return None
        """

class Orders(SPAPIBase):
    def getOrders(self,CreatedAfter,OrderStatuses):
        endpoint = "/orders/v0/orders"
        self.params.update({"CreatedAfter": CreatedAfter,
                            "OrderStatuses":OrderStatuses})  
        payload = super().execute_request(endpoint=endpoint,params=self.params,payload='payload',method='get')
        return payload.get('Orders')

    def getOrder(self,orderId):
        endpoint = f"/orders/v0/orders/{orderId}"
        self.params.update ({"orderId" : orderId})
        return super().execute_request(endpoint=endpoint,params=self.params,payload='payload',method='get')
    
    def getOrderBuyerInfo(self,orderId):
        endpoint = f"/orders/v0/orders/{orderId}/buyerInfo"
        self.params.update ({"orderId" : orderId})
        return super().execute_request(endpoint=endpoint,params=self.params,method='get')
    
    def getOrderAddress(self,):
        pass 

    def getOrderItems(self,):
        pass

    def getOrderItemsBuyerInfo(self,):
        pass

    def updateShipmentStatus(self,):
        pass

    def getOrderRegulatedInfo(self,):
        pass

    def updateVerificationStatus(self,):
        pass

    def confirmShipment(self,):
        pass
    

class Reports(SPAPIBase):
    # https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-reference        
    def createReport(self,reportType,reportOptions=None,dataStartTime=None,dataEndTime=None):
        endpoint = '/reports/2021-06-30/reports'
        data = {"reportType":reportType,
                "reportOptions" : reportOptions,
                "marketplaceIds" : [self.marketplace_id],
                "dataStartTime" : dataStartTime,
                "dataEndTime" : dataEndTime}
        return super().execute_request(method='post',endpoint=endpoint,json_input=data)
    
    def getReports(self,reportTypes=None,processingStatuses=None,marketplaceIds=None,
                   pageSize=None,createdSince=None,CreatedUntil=None,nextToken=None):
        endpoint = "/reports/2021-06-30/reports"
        self.params.update({ 
            "reportTypes" : reportTypes,
            "processingStatuses" : processingStatuses,
            "marketplaceIds" : marketplaceIds,
            "pageSize" : pageSize,
            "cretedSince" : createdSince,
            "createdUntil" : CreatedUntil,
            "nextToken" : nextToken
            })
        response = super().execute_request(endpoint=endpoint,params=self.params,payload='reports',method='get')
        return response
    
    def getReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
        return super().execute_request(endpoint=endpoint,params=self.params,method='get')

    def cancelReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
        return super().execute_request(endpoint=endpoint,params=self.params,method='delete')

    def getReportSchedules(self,reportTypes):
        endpoint = "/reports/2021-06-30/schedules"
        self.params.update({"reportTypes" : reportTypes})
        return super().execute_request(endpoint=endpoint,params=self.params,method='get')

    def createReportSchedule(self):
        endpoint = f"/reports/2021-06-30/schedules"

    def getReportSchedule(self,reportScheduleId):
        endpoint = f"/reports/2021-06-30/schedules/{reportScheduleId}"

    def cancelReportSchedule(self,reportScheduleId):
        endpoint = f"/reports/2021-06-30/schedules/{reportScheduleId}"

    def getReportDocument(self,reportDocumentId):
        endpoint = f"/reports/2021-06-30/documents/{reportDocumentId}"
        self.params.update({"reportDocumentId" : reportDocumentId})
        return super().execute_request(endpoint=endpoint,params=self.params)
        




class Shipping(SPAPIBase):
    pass
