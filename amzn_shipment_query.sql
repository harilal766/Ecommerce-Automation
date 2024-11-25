
            SELECT DISTINCT
            amazon-order-id, purchase-date, last-updated-date, order-status, product-name,item-status, quantity, item-price, item-tax, shipping-price, shipping-tax 
            FROM Orders 
            WHERE amazon_order_id IN 
                	('408-2207105-8185144', '171-2860293-4573126', '405-5142500-8749156', '405-5684197-8263504', '405-4471990-3110724', '407-0749928-3148341', '171-7906369-9845952', '407-6478206-4772334', '406-5202604-5197163', '408-2937479-4182750', '406-9842547-5707502', '407-3594126-7517156', '405-2890357-6694768', '408-7470107-3753964', '407-5062014-7214742', '408-3619872-6041103', '402-7761907-9018739')
            ORDER BY product_name asc,quantity asc;
        