from helpers.sql_scripts import sql_table_CR
from helpers.file_ops import *
from sales.views import *








def order_tester():
    ord_ins = Orders()
    rep = ord_ins.getOrders(CreatedAfter=iso_8601_timestamp(2),OrderStatuses="Unshipped")
    print(rep)




    
    

        