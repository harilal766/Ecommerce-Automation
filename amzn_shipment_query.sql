
            SELECT DISTINCT
            name,paid_at,fulfillment_status,subtotal,shipping,taxes,total,lineitem_quantity,lineitem_name,lineitem_price,lineitem_compare_at_price 
            FROM sh_orders 
            WHERE name IN (
                	
            )
            ORDER BY lineitem_name ASC, lineitem_price ASC;
        