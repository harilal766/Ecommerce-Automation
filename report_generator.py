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


ord_ins = Orders(); created_after = (datetime.utcnow() - timedelta(days=7)).isoformat()
ord_resp = ord_ins.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")
orders = sp_api_shipment_summary(response=ord_resp)
cod_order_ids = orders.cod; prepaid_order_ids = orders.prepaid



def report_driver(report_type): 
    report_type = report_type.lower()

    if "report" in report_type:
        from manual_testing import query_execution
        query_execution(filter_rows=cod_order_ids)
        

