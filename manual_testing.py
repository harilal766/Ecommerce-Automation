from helpers.sql_scripts import sql_table_CR
from helpers.messages import *
from amazon.response_manipulator import *
from amazon.sp_api_utilities import *


# time is must, if days == 0 , treat time as of todays
# for normal timestamp, there shouldnt be much parameters
# if date is needed only and not time type is not needed.
def timestamp(days,type=None,split=None):
    # types : iso 8601, 
    ind_timestamp = (datetime.now(timezone("Asia/Kolkata"))-timedelta(days=days))
    if type == "iso":
        return ind_timestamp.isoformat()
    elif type == "utc":
        return ind_timestamp.utcnow()
    # if the split is none, return the full time stamp


print(timestamp(0,type="iso"))

print(iso_8601_timestamp(0))














































def amazon_shipment_report():
    """"
    Step 1 - Order API access
        1. Access the order api and access the shipped (scheduled) and pending pickup orders.
        2. append the cod and prepaid orders in to seperate lists.

    Step 2 - Report API Access
        1. Request the report api based on the scheduled orders type,starting from 5 days ago to today.
        2. filter the received df based on required fields.
        3. with the help of a for loop,
            filter the df again based on the previous cod and prepaid lists and convert it to an excel sheet 
            the sheet names need to be dynamic in future.
    """
    context = {"path" : None, "status":None }
    # go to api docs and find other order statueses like waiting for pickup
    order_instance = Orders()
    todays_timestamp = iso_8601_timestamp(0); todays_ind_date = iso_8601_timestamp(0)
    try:
        # since amazon's time limit for daily orders is 11 am , make \\
        # context initialization for Django...
        context = {"path" : None}
        #next_ship = amzn_next_ship_date().split("T")[0]
        next_ship = todays_ind_date
        """
        last ship date needed to be stored in the database to avoid logical errors 
        if the scheduling report taking is being done after 11 am. 
        """
        orders_details = order_instance.getOrders(CreatedAfter=from_timestamp(7),OrderStatuses="Shipped")
        space = " "*14
        color_text(message=f"Orders  Count : {len(orders_details)}")
        cod_orders = []; prepaid_orders = []; order_count = 0
        if isinstance(orders_details,list) and len(orders_details) != 0:
            color_text(message=f"Orders scheduled for {todays_ind_date}")
            for i in orders_details:
                if isinstance(i,dict):
                    # order fields
                    order_id = i["AmazonOrderId"]; 
                    purchase_date = i["PurchaseDate"]; ship_date = i["LatestShipDate"]
                    payment_method = i["PaymentMethod"]; status = i["EasyShipShipmentStatus"]
                    # verify again to get orders for today only
                    if (ship_date.split("T")[0] == next_ship.split("T")[0]) and status == "PendingPickUp" and ship_date == next_ship:
                        order_count += 1
                        if payment_method == "COD":
                            cod_orders.append(order_id)
                        else:
                            prepaid_orders.append(order_id)
                        order_info = f"{order_count}.{order_id} : Status - {status}, puchased - {purchase_date}, shipping on - {ship_date}, type - {payment_method}, date : {next_ship}"
                        print(order_info)
                else:
                    color_text(message=f"Not a dictionary but of type : {type(i)} ",color="red")
        else:
            color_text(message=f"No pending schedules for {todays_timestamp.split("t")[0]}",color="red")
    except Exception as e:
        better_error_handling(e)

