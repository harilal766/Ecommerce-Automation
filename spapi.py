from amazon.authorization import *
from amazon.sp_api_models import *
from amazon.response_manipulator import *

def amzn_ship_date_finder():
    if datetime.now().time().hour >= 11:
    # if the time is past 11:00 AM and todays scheduling is done, return tomorrows date if not a holiday
        return iso_8601_timestamp(-1)
    else:
        return iso_8601_timestamp(0)
    
def view():
    R = Reports(); O = Orders()
    orders = O.getOrders(CreatedAfter=iso_8601_timestamp(4),LatestShipDate=amzn_ship_date_finder(),
                                OrderStatuses="Unshipped")
    cod = [] ; prepaid = []
    for i in orders:
        if isinstance(i,dict):
            if i['LatestShipDate'].split("T")[0] == amzn_ship_date_finder().split("T")[0]:
                #print(f"{i["AmazonOrderId"]} - {i['LatestShipDate']}")
                if i["PaymentMethod"] == "COD":
                    cod.append(i["AmazonOrderId"])
                else:
                    prepaid.append(i["AmazonOrderId"])
    print(cod,prepaid)

    tablename="Amazon" ; dbname = "Orders"; db_system = "sqlite"
    df = sp_api_report_df_generator(report_type=order_report_types["datewise orders data flatfile"],
                                start_date=iso_8601_timestamp(5),end_date=iso_8601_timestamp(0))
    df.to_sql(name=tablename,con=db_connection(dbname=dbname,db_system=db_system),
                  if_exists='replace',index=False)

view()