
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'402-0385650-7901143','403-9295536-3251527','403-2770385-6015537',
'406-7203102-2217958','408-0778729-6489112','408-4560316-2058748',
'406-6358237-0895523','406-6015826-4578752','403-9783460-2711515',
'403-8199928-6255561','404-6553736-9505110','405-3546933-5553919',
'403-6957372-3452365','402-9597525-5496351','408-7358176-9802750',
'405-6116372-6543514','406-8025826-3887524','404-4524849-4479542'
            )
            ORDER BY product_name asc,quantity asc;
        