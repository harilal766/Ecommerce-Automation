
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'402-3133872-6654715','403-3300760-4441946','171-5234487-2853927',
'405-0119420-2145178','404-8917232-7561901','406-7717888-1251546',
'403-9096037-8805967','405-1714148-8506719','407-8455001-8761934',
'408-0564092-9606764','408-0014961-1068362','402-0291247-4523523',
'407-7505368-8549939','402-9101599-0007546','171-4099821-9745122',
'171-6951987-1292334','408-1538265-5224349','404-7309481-5384344',
'407-7971101-6865946'
            )
            ORDER BY product_name asc,quantity asc;
        