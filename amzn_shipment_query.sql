
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'403-1082177-4218763','406-3690667-9537104','407-7592308-7339558',
'404-1384539-9448331','171-6213321-7831543','404-8417825-3359542',
'171-9256379-1958735','407-6182137-3377951','408-7547680-0270758',
'405-1722293-3690753','408-1604269-7942766','403-4744654-9715566',
'171-1366642-2514727','407-4065966-0525963','402-4067307-2411563',
'408-2317669-4686759','402-7275967-4902750','408-3151122-0513962'
            )
            ORDER BY product_name asc,quantity asc;
        