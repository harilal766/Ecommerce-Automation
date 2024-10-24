
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'402-6032157-5743564','171-5530058-6690713','403-2487054-1247560',
'402-8801079-4362746','404-9006096-9549910','408-2622139-3509109',
'405-1821662-7273140','404-9815509-7533154','171-3418552-4165930',
'403-8237483-5421932','171-1478597-9493911','403-5135155-1905901',
'406-5252063-1014754','402-9903729-0929158','402-1896289-8183516',
'406-9317790-0259557','402-4361601-5005946','404-4527322-4199551',
'408-4502211-0015524',
            )
            ORDER BY product_name asc,quantity asc;
        