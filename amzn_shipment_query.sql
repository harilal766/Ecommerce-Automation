
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'405-4895004-1467556','407-0194447-8272305','402-3443698-7195568',
'405-5777953-0321926','406-0406214-0143520','408-9014465-8651534',
'404-3725580-4374726','171-2249234-3601164','403-3758736-1413128',
'407-0648164-8457169','406-1430268-9161915','402-6536218-9649925',
'405-2007570-0034728','408-0263146-1054705'
            )
            ORDER BY product_name asc,quantity asc;
        