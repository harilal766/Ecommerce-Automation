
            SELECT DISTINCT
            amazon_order_id,purchase_date,last_updated_date,order_status,product_name, quantity,item_price,item_tax,shipping_price,shipping_tax 
            FROM sh_orders 
            WHERE amazon_order_id IN (
                	
            )
            ORDER BY product_name ASC, item_price ASC
            ;
        