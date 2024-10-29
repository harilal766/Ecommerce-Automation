/* "Cash On Delivery Transactions and Non-Transactional Fees", "Electronic Transactions (Credit Card/Net Banking/GC)" */
select distinct
	amazon_order_id, purchase_date,order_status,product_name,
	date as settlement_date,product_details, total_product_charges,amazon_fees,other,total_inr
	from 
	orders left join transactions
	on orders.amazon_order_id = transactions.order_id
	where amazon_order_id = '171-0330299-6925938'
	order by purchase_date asc, amazon_order_id asc
	;