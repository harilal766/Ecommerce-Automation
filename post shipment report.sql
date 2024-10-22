
            SELECT DISTINCT
             Name, Financial_Status, Paid_at, Fulfillment_Status, Fulfilled_at, Subtotal, Shipping, Total, Lineitem_quantity, Lineitem_name,
                    Lineitem_price, Lineitem_compare_at_price, Shipping_Province_Name, 
            FROM sh_orders 
            WHERE name IN (
                	
            )
            ORDER BY lineitem_name ASC, lineitem_price ASC;
        