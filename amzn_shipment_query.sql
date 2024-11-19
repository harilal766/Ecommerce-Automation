
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'407-8398850-2780356','403-2237117-8000309','405-5565914-4118722',
'404-7505534-1309915','171-8444621-9617952','404-0249913-0126726',
'406-6835753-6387502','407-3633226-6703537','408-5066918-6822713',
'403-9162716-6359506'
            )
            ORDER BY product_name asc,quantity asc;
        