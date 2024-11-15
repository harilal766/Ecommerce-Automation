
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'406-3553314-4605151','402-5723375-7457118','408-4489624-0607563',
'402-0129270-7107516','408-8017862-9185965','171-7144643-5981909',
'408-6130004-1914764','402-1994360-0828317','171-0782460-3552339',
'408-0883229-4285136','402-4117206-7474728','406-7095074-9434739',
'402-8578467-9485126','405-3167821-6585934'
            )
            ORDER BY product_name asc,quantity asc;
        