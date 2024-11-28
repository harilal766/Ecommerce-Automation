from amazon.authorization import *
from amazon.api_models import *
from amazon.response_manipulator import *


ord_ins = Orders(); created_after = (datetime.utcnow() - timedelta(days=4)).isoformat()
ord_resp = ord_ins.getOrders(CreatedAfter=created_after,OrderStatuses="Unshipped")
print(amazon_dashboard(response=ord_resp))