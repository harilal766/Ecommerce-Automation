import requests
from datetime import datetime, timedelta, timezone
from helpers.messages import color_text
from helpers.file_ops import *
from amazon.authorization import *
import time

created_after = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()


normal_endpoint = "https://sellingpartnerapi-eu.amazon.com"
sandbox_endpoint = "https://sandbox.sellingpartnerapi-eu.amazon.com"
import logging
import requests

class SPAPIBase:
    def __init__(self,base_url=normal_endpoint,marketplace_id="A21TJRUUN4KGV"):
        self.access_token = get_or_generate_access_token()
        self.base_url = base_url
        self.marketplace_id = marketplace_id
        self.headers = {
            "Authorization" : "access token",
            "x-amz-access-token": self.access_token,
            "Content-Type": "application/json",
            "Connection" : "keep-alive",
            "Accept": "application/json"
            }
        # Common parameters, individual ones will be added from the respective functions
        self.params = {
            "MarketplaceIds": self.marketplace_id,
        }
        self.success_codes = {200,201}

    def execute_request(self,endpoint,method,burst,json_input=None,params=None,payload=None):
        retry = 5; delay=1
        # detecting burst limit should have top priority...
        for request_count in range(burst):
            try:
                # make sure the endpoint have a "/" at the begining and does not end with "/"
                if endpoint[0] != '/':
                    endpoint = '/'+endpoint
                status_end = " | "
                url = self.base_url+endpoint

                if method.lower() == 'get':
                    response = requests.get(url, headers=self.headers,params = params,timeout=10)
                elif method.lower() == 'post':
                    response = requests.post(url, headers=self.headers,json = json_input,timeout=10)
                elif method.lower() == 'delete':
                    response = requests.delete(url, headers=self.headers,timeout=10)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                rate_limit = response.headers.get('x-amzn-RateLimit-Limit',None)
                if rate_limit not in [0,None]  :
                    color_text(message=f"Rate limit : {rate_limit}",color="red")
                else:
                    color_text(message=f"Api limit reached.",color="red")
                #color_text(message=response.headers,color="red")
                
                if request_count == burst:
                    color_text(message="Burst Limit reached",color="red")

                if response.status_code == 429:
                    delay *=2
                    time.sleep(delay)
                    color_text(message=f"Rate limit reached, retrying in {delay} seconds.",color='red')
                elif response.status_code >= 400:
                    response.raise_for_status()
                else:
                    color_text(message=request_count,color="red")
                    request_count += 1
                    time.sleep(float(rate_limit)) # to delay based on the rate limit which is negligible
                    response_data = response.json()
                    return response_data.get(payload,None) if payload else response_data
                
            except AttributeError as e:
                color_text(message=f"Attribute Error Found : {e}\n{response}\n-----------------------------------",color='red')
                break
            except requests.exceptions.RequestException as e:
                better_error_handling(f"Error : {e}")
                break
        return None

class Orders(SPAPIBase):
    def getOrders(self,CreatedAfter=None,CreatedBefore=None,
                  OrderStatuses=None,
                  LastUpdatedAfter=None,
                  PaymentMethods=None,EasyShipShipmentStatuses=None,
                  EarliestShipDate=None,LatestShipDate=None):
        

        """
        Note: Either the CreatedAfter parameter or the LastUpdatedAfter parameter is required.
        Both cannot be empty. CreatedAfter or CreatedBefore cannot be set when LastUpdatedAfter is set.

        Note: LastUpdatedBefore is optional when LastUpdatedAfter is set. But if specified, LastUpdatedBefore
        must be equal to or after the LastUpdatedAfter date and at least two minutes before current time.
        
        Possible values of EasyShipShipmentStatuses :
        - PendingSchedule (The package is awaiting the schedule for pick-up.)
        - PendingPickUp (Amazon has not yet picked up the package from the seller.)
        - PendingDropOff (The seller will deliver the package to the carrier.)
        - LabelCanceled (The seller canceled the pickup.)
        - PickedUp (Amazon has picked up the package from the seller.)
        - DroppedOff (The package is delivered to the carrier by the seller.)
        - AtOriginFC (The packaged is at the origin fulfillment center.)
        - AtDestinationFC (The package is at the destination fulfillment center.)
        - Delivered (The package has been delivered.)
        - RejectedByBuyer (The package has been rejected by the buyer.)
        - Undeliverable (The package cannot be delivered.)
        - ReturningToSeller (The package was not delivered and is being returned to the seller.)
        - ReturnedToSeller (The package was not delivered and was returned to the seller.)
        - Lost (The package is lost.)
        - OutForDelivery (The package is out for delivery.)
        - Damaged (The package was damaged by the carrier.)
        
        """
        endpoint = "/orders/v0/orders"
        self.params.update({"CreatedAfter" : CreatedAfter,
                            "CreatedBefore" : CreatedBefore,
                            "OrderStatuses": OrderStatuses,
                            "LastUpdatedAfter" : LastUpdatedAfter,
                            "PaymentMethods" : PaymentMethods,
                            "EarliestShipDate" : EarliestShipDate, "LatestShipDate" : LatestShipDate,
                            "EasyShipShipmentStatuses" : EasyShipShipmentStatuses}) 
         
        """
        Note: Either the CreatedAfter parameter or the LastUpdatedAfter parameter is required.
        Both cannot be empty. CreatedAfter or CreatedBefore cannot be set when LastUpdatedAfter is set.
        """
        if (CreatedAfter != None) or (LastUpdatedAfter != None):
            response = super().execute_request(endpoint=endpoint,params=self.params,
                                            payload='payload',method='get',burst=20)
            
            #color_text(message=f"{response}\n+++++++++++++++++",color="blue")
            return response.get("Orders",None)
        elif CreatedAfter == None and LastUpdatedAfter == None:
            color_text(message="Either the CreatedAfter parameter or the LastUpdatedAfter parameter is required Both cannot be empty",color="red")
            return None

    def getOrder(self,orderId):
        endpoint = f"/orders/v0/orders/{orderId}"
        self.params.update ({"orderId" : orderId})
        return super().execute_request(endpoint=endpoint,params=self.params,
                                       payload='payload',method='get',burst=30)
    
    def getOrderBuyerInfo(self,orderId):
        endpoint = f"/orders/v0/orders/{orderId}/buyerInfo"
        self.params.update ({"orderId" : orderId})
        return super().execute_request(endpoint=endpoint,params=self.params,method='get',burst=30)
    
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
        return super().execute_request(method='post',endpoint=endpoint,
                                       json_input=data,burst=15)
    
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
        response = super().execute_request(endpoint=endpoint,params=self.params,
                                           payload='reports',method='get',burst=10)
        return response
    
    def getReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
        return super().execute_request(endpoint=endpoint,params=self.params,
                                       method='get',burst=15)

    def cancelReport(self,reportId):
        endpoint = f"/reports/2021-06-30/reports/{reportId}"
        self.params.update({"reportId" : reportId})
        return super().execute_request(endpoint=endpoint,params=self.params,
                                       method='delete',burst=10)

    def getReportSchedules(self,reportTypes):
        endpoint = "/reports/2021-06-30/schedules"
        self.params.update({"reportTypes" : reportTypes})
        return super().execute_request(endpoint=endpoint,params=self.params,
                                       method='get',burst=10)

    def createReportSchedule(self):
        endpoint = f"/reports/2021-06-30/schedules"

    def getReportSchedule(self,reportScheduleId):
        endpoint = f"/reports/2021-06-30/schedules/{reportScheduleId}"

    def cancelReportSchedule(self,reportScheduleId):
        endpoint = f"/reports/2021-06-30/schedules/{reportScheduleId}"

    def getReportDocument(self,reportDocumentId):
        endpoint = f"/reports/2021-06-30/documents/{reportDocumentId}"
        self.params.update({"reportDocumentId" : reportDocumentId})
        return super().execute_request(endpoint=endpoint,params=self.params,
                                       method='get',burst=15)
        




class Shipping(SPAPIBase):
    pass
