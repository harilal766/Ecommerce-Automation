select distinct
	orders.purchase_date,
	date as transaction_date,order_id,transaction_type,product_details, total_product_charges,amazon_fees,other,total_inr
	from 
	transaction_prepaid join orders
	on order_id = amazon_order_id
	where date between '2024-10-04' and '2024-10-05'
	order by orders.purchase_date asc,order_id asc
	;