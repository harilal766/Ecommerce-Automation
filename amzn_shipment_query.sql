
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'406-5483064-8506731','402-9000063-9763569','402-3665415-5801101',
'405-8894014-3504345','403-8496059-2945937','405-9226321-0183557',
'407-6099423-4087560','407-3338838-3041107','406-6071418-0720325',
'403-2383220-3678724','402-4748471-0429966','402-3407502-7669905',
'171-9652860-5389936','404-5015362-7465168','407-6544112-0311518',
'408-0479139-9604346','405-6430185-9377931','407-7750328-0759531'
            )
            ORDER BY product_name asc,quantity asc;
        