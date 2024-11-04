
            SELECT DISTINCT
             Name, Financial_Status, Paid_at, Fulfillment_Status, Fulfilled_at, Subtotal, Shipping, Total, Lineitem_quantity, Lineitem_name,
                    Lineitem_price, Lineitem_compare_at_price, Shipping_Province_Name, 
            FROM sh_orders 
            WHERE name IN (
                	'#10737','#10738','#10739',
'#10740','#10741','#10742',
'#10743','#10744','#10745',
'#10746','#10748','#10747',
'#10749','#10750','#10751',
'#10752','#10753','#10754',
'#10756','#10755','#10758',
'#10757','#10759','#10760',
'#10762','#10761','#10764',
'#10763','#10765','#10766',
'#10768','#10767','#10769',
'#10770','#10771','#10772',
'#10773','#10774','#10775'
            )
            ORDER BY lineitem_name ASC, lineitem_price ASC;
        