
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'408-8323894-9791516','406-2206875-0560312','406-9007521-9371529',
'402-0660961-1651530','405-9038317-2517124','408-9877398-5305900',
'171-0846488-3349162','171-0463988-6887546','405-7309175-9812301',
'408-7227108-1868366','403-8020862-6547546','402-3931916-8568340'
            )
            ORDER BY product_name asc,quantity asc;
        