
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	
            )
            ORDER BY product_name asc,quantity asc;
        