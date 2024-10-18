

COPY settlement_tax_breakup_cod 
(
	settlement_id ,settlement_start_date ,settlement_end_date ,deposit_date, 
	totalamount,transaction_type,order_id ,amount_type,amount_description ,
	amount ,fulfillment_id ,posted_date,
	posted_date_time ,	quantity_purchased
	)
FROM 'D:\Automation\SQL Test\27.9.24 - 4.10.24 Tax breakup COD.csv'
DELIMITER ','
CSV HEADER;
