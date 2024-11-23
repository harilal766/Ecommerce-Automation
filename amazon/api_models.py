import requests
from datetime import datetime, timedelta, timezone
from helpers.messages import color_text
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
        status_end = " -> "
        # Since majority of methods are GET,...
        if method == None:
            color_text(message=f"GET ⬇️ ",color='blue',end=status_end)
            response = requests.get(self.base_url+endpoint, headers=self.headers,params = params)
        elif method == 'post':
            color_text(message=f"POST ⬆️ ",color='blue',end=status_end)
            response = requests.post(self.base_url+endpoint, headers=self.headers,json = json_input)
        elif method == 'delete':
            color_text(message=f"DELETE 🚮 ",color='red',end=status_end)
            response = requests.delete(self.base_url+endpoint, headers=self.headers)

        success_codes = [200,202]
        forbidden_codes = [403]
        error_codes = [400,401,404,415,429,500,503]

        status_color = 'red' ; 
        if response.status_code in success_codes :
            status_color = 'green'
            color_text(message=f"{response.status_code}",color=status_color,end=status_end)
            response.raise_for_status()
            response = response.json()

        if payload == None:
            return response
        else :
            return response[payload]


class Orders(SPAPIBase):
    def getOrders(self,CreatedAfter,OrderStatuses):
        endpoint = "/orders/v0/orders"
        self.params.update({"CreatedAfter": CreatedAfter,
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
        return super().response_processor(method='post',endpoint=endpoint,json_input=data)
    
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
        response = super().response_processor(endpoint=endpoint,params=self.params,payload='reports')
        return response
    
    def getReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
        return super().response_processor(endpoint=endpoint,params=self.params)

    def cancelReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
        return super().response_processor(endpoint=endpoint,params=self.params,method='delete')

    def getReportSchedules(self,reportTypes):
        endpoint = "/reports/2021-06-30/schedules"
        self.params.update({"reportTypes" : reportTypes})
        return super().response_processor(endpoint=endpoint,params=self.params)

    def createReportSchedule(self):
        endpoint = f"/reports/2021-06-30/schedules"

    def getReportSchedule(self,reportScheduleId):
        endpoint = f"/reports/2021-06-30/schedules/{reportScheduleId}"

    def cancelReportSchedule(self,reportScheduleId):
        endpoint = f"/reports/2021-06-30/schedules/{reportScheduleId}"

    def getReportDocument(self,reportDocumentId):
        endpoint = f"/reports/2021-06-30/documents/{reportDocumentId}"
        self.params.update({"reportDocumentId" : reportDocumentId})
        return super().response_processor(endpoint=endpoint,params=self.params)
        




class Shipping(SPAPIBase):
    pass
