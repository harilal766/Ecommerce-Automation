
            SELECT DISTINCT
             Name, Financial_Status, Paid_at, Fulfillment_Status, Fulfilled_at, Subtotal, Shipping, Total, Lineitem_quantity, Lineitem_name,
                    Lineitem_price, Lineitem_compare_at_price, Shipping_Province_Name, 
            FROM sh_orders 
            WHERE name IN (
                	'#13673','#13672','#13670',
'#13671','#13668','#13669',
'#13667','#13666','#13664',
'#13665','#13663','#13662',
'#13661','#13660','#13659',
'#13658','#13657','#13656',
'#13655','#13654','#13653',
'#13652','#13651','#13650',
'#13649','#13648','#13647',
'#13646','#13645','#13644',
'#13643','#13642','#13640',
'#13641','#13639','#13638',
'#13637','#13636','#13635',
'#13634','#13632','#13633',
'#13631','#13630','#13629',
'#13628','#13627','#13626',
'#13624','#13625','#13623',
'#13622','#13620','#13621',
'#13619','#13618','#13616',
'#13617','#13615','#13614',
'#13613','#13612','#13611',
'#13610','#13609','#13608',
'#13607','#13606','#13605',
'#13604','#13603','#13602',
'#13601','#13600','#13598',
'#13599','#13597','#13596',
'#13595','#13594','#13592',
'#13593','#13591','#13590',
'#13588','#13589','#13586',
'#13587','#13585','#13584',
'#13583','#13582','#13581',
'#13580','#13579','#13578'
            )
            ORDER BY lineitem_name ASC, lineitem_price ASC;
        