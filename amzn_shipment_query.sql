
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'402-1625363-0997104','404-6529373-5270753','171-9454776-2827554',
'405-1541921-1565900','407-4214835-3285110','408-7609871-0723550',
'407-2270709-0813110','403-7804454-1849130','402-2797819-3896315',
'402-9997684-4041903','407-6880135-3327568','408-1559314-3982740',
'405-4862767-1427510','408-0807448-0394749','404-4995495-3445115',
'408-6648024-0043514','408-0217604-4025943','402-8397302-0140360',
'404-3549069-5649912'
            )
            ORDER BY product_name asc,quantity asc;
        