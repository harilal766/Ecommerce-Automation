
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'171-4811662-2491565','406-9843594-5635558','402-5226769-2085968',
'408-4427887-7099548','407-4908374-7341119','406-4274111-9899510',
'403-9745109-0484361','408-8311747-6025169','402-1751527-0530702',
'408-1194548-7554750','407-2078866-2165149','403-2421636-8149937',
'406-3906557-2413128','407-3618290-7967514','402-3080972-7603509',
'407-8716367-4538735','405-7301683-8488345','407-8324469-8413942',
'406-9055595-5100365'
            )
            ORDER BY product_name asc,quantity asc;
        