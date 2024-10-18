/*
	Table : Orders
	------------------------------------------------
	Table : Settlement_transactions_cod
	Fields : Date, Transaction_type, Order_ID, Product_Details, Total_product_charges, Total_promotional_rebates, Amazon_fees, Other, Total_INR
	--------------------------------------------------
	Table : Settlement_tax_breakup_cod
*/
select 
	/*Order table*/
	distinct
	settlement_transactions_cod.Date as transaction_date, purchase_date, order_id, Transaction_type, Product_Details,
	Total_product_charges, Amazon_fees, Other, Total_INR
	from 
	orders join settlement_transactions_cod  
		on orders.amazon_order_id = settlement_transactions_cod.order_id
	where 
		settlement_transactions_cod.Date between '4.10.24' and '5.10.24'
	order by 
		date asc, order_id
;

