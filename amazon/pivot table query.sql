select amazon_order_id,last_updated_date,order_status ,product_name ,sum(quantity) as total_quantity
	from orders 
	where last_updated_date like '%2024-11-05%' 
	and 
	quantity = 1
	and 
	order_status ='Pending - Waiting for Pick Up'
	group by product_name,quantity;