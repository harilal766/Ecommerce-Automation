from amazon.response_manipulator import n_days_timestamp,sp_api_report_df_generator
from helpers.file_ops import *
from amazon.report_types import *


file_dir = dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
filename=f"16 - 23.csv"


from helpers.sql_scripts import db_connection,sql_table_CR
from report_generator import *
from amazon.api_models import *
from amazon.response_manipulator import *
import pandas as pd



def api_report_gen():
    try:
        tablename = "QQQ"
        # converting the data to sql for querying
        df = sp_api_report_df_generator(report_type=order_report_types["datewise orders data flatfile"],
                                start_date=n_days_timestamp(7),end_date=n_days_timestamp(0))

        df.to_sql(name=tablename,con=db_connection(dbname="Amazon",db_system='sqlite'),if_exists= 'replace',index=False)

        # querying the sql table and finding cod and prepaid reports seperately
        ord_ins = Orders(); created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()
        ord_resp = ord_ins.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")
        orders = sp_api_shipment_summary(response=ord_resp)

        cod_order_ids = orders.cod; prepaid_order_ids = orders.prepaid
        fields = """amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax"""
        database = "Amazon" ; out_excel_path=dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
        """
        query = filter_query_generator(
                    fields = "*",
                    table=tablename, id = "amazon-order-id",order_by_clause="product-name asc,quantity asc",
                    sql_filename="amzn-shipment-query",
                    order_ids=cod_order_ids
                )
        """
        query = f"SELECT {fields} FROM {tablename} where amazon_order_id in {tuple(cod_order_ids)};"
        print(query)
        pass

        # connecting to the db
        connection = db_connection(dbname=database,db_system="sqlite")
        if connection:
            success_status_msg("Connection Succeeded.")
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
        else:
            color_text(message="Connection Failed",color="red")

        # converting the sql result into excel file
        sql_to_excel(sql_cursor=cursor,query_result=results,out_excel_path=out_excel_path)

    except Exception as e:
        better_error_handling(e)

api_report_gen()