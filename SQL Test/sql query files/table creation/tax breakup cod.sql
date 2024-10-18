
CREATE TABLE Settlement_Tax_Breakup_COD (
	settlement_id BIGINT,
	settlement_start_date TIMESTAMPTZ,
	settlement_end_date TIMESTAMPTZ,
	deposit_date TIMESTAMPTZ,	
	totalamount	NUMERIC(10,2),
	transaction_type VARCHAR(20),
	order_id VARCHAR(20),
	amount_type	VARCHAR(20),
	amount_description VARCHAR(50),
	amount NUMERIC(10,2),
	fulfillment_id VARCHAR(25),
	posted_date	DATE,
	posted_date_time TIMESTAMPTZ,	
	quantity_purchased INTEGER
);