
            SELECT DISTINCT
             Name, Financial_Status, Paid_at, Fulfillment_Status, Fulfilled_at, Subtotal, Shipping, Total, Lineitem_quantity, Lineitem_name,
                    Lineitem_price, Lineitem_compare_at_price, Shipping_Province_Name, 
            FROM sh_orders 
            WHERE name IN (
                	'#12923','#12924','#12928',
'#12929','#12935','#12936',
'#12939','#12942','#12943',
'#12944','#12945'
            )
            ORDER BY lineitem_name ASC, lineitem_price ASC;
        