from amazon.authorization import *
from amazon.sp_api_models import *
from amazon.response_manipulator import *
from helpers.sql_scripts import *
from sales.views import *



def amazon_reports():
    try:
        R = Reports(); O = Orders()
        orders = O.getOrders(CreatedAfter=iso_8601_timestamp(4),LatestShipDate=amzn_next_ship_date(),
                                    OrderStatuses="Unshipped")
        cod = [] ; prepaid = []
        for i in orders:
            next_ship_date = datetime.strptime(amzn_next_ship_date().split("T")[0], "%Y-%m-%d")
            latest_ship_date = datetime.strptime(i['LatestShipDate'].split("T")[0], "%Y-%m-%d")
            if isinstance(i,dict):
                if next_ship_date == latest_ship_date:
                    #print(f"{i["AmazonOrderId"]} - {i['LatestShipDate']}")
                    if i["PaymentMethod"] == "COD":
                        cod.append(i["AmazonOrderId"])
                    else:
                        prepaid.append(i["AmazonOrderId"])

        orders = {"cod":cod,"prepaid" : prepaid}

        dbname = "Amazon" ;tablename="Orders" ; db_system = "sqlite"; out_excel_dir = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
        df = sp_api_report_df_generator(report_type=order_report_types["datewise orders data flatfile"],
                                    start_date=iso_8601_timestamp(5),end_date=iso_8601_timestamp(0))
        if df is not None and not df.empty:
            df.to_sql(name=tablename,con=db_connection(dbname=dbname,db_system=db_system),
                        if_exists='replace',index=False)
        
            for type,value in orders.items():
                execution = filter_query_execution(dbname=dbname,db_system=db_system,tablename=tablename,
                                                filter_rows=value)
                sql_to_excel(sql_cursor=execution[0],query_result=execution[1],
                            out_excel_path=out_excel_dir,excel_filename=f"{amzn_next_ship_date().split("T")[0]}-{type}")
                
                context = {"path" : out_excel_dir}
            return context
# ERRORS ----------------------------------------------------------------------------------------------------------
        else:
            return print("Dataframe is empty")
    except Exception as e:
        better_error_handling(e)