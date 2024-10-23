
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'402-1353443-1517131','408-3285884-1565915','403-5968591-1533952',
'408-0280581-3066722','404-7562859-7323503','403-3895464-2925955',
'407-4009818-8021165','404-0531426-9984319','407-3190113-0251552',
'405-3473074-9892304','171-1795120-8493949','406-9148608-1522741',
'408-5849436-5457115','406-8495799-1101110','404-0747751-6466723',
'171-4266933-8196350','403-9547142-2484349',
            )
            ORDER BY product_name asc,quantity asc;
        