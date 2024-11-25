from helpers.file_ops import *
from helpers.sql_scripts import query_backup,line_limit_checker,sql_to_excel,db_connection,sql_table_CR
from helpers.loading_animations import loading_animation
from helpers.regex_patterns import *
"""
    make the query for filtering orders form sql table bsaed on seperate cod and non cod pdf files
"""

"""
    finally:
        success_status_msg(shipment_report_query)
        # closing the db
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and connection:
            connection.close()
"""

# Driver code for report generator
# querying the sql table and finding cod and prepaid reports seperately

from amazon.api_models import *
from amazon.response_manipulator import *
from manual_testing import filter_query_execution

ord_ins = Orders(); created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()
ord_resp = ord_ins.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")
orders = sp_api_shipment_summary(response=ord_resp)
cod_order_ids = orders.cod; prepaid_order_ids = orders.prepaid

tablename = "Orders"; dbname="Amazon"; db_system = "sqlite"

def report_driver(report_type): 
    report_type = report_type.lower()

    if "report" in report_type:
                # converting the data to sql for querying
        df = sp_api_report_df_generator(report_type=order_report_types["datewise orders data flatfile"],
                                start_date=n_days_timestamp(7),end_date=n_days_timestamp(0))
        df.to_sql(name=tablename,con=db_connection(dbname=db_connection,db_system=db_system),
                  if_exists= 'replace',index=False)
        
        filter_query_execution(dbname=dbname,tablename=tablename,db_system=db_system,
                               filter_rows=cod_order_ids)
        filter_query_execution(dbname=dbname,tablename=tablename,db_system=db_system,
                               filter_rows=prepaid_order_ids)
        

