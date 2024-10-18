
CREATE TABLE Transaction_prepaid (
	Date DATE,
	Transaction_type VARCHAR(50),
	Order_ID VARCHAR(20),
	Product_Details VARCHAR(100),
	Total_product_charges	NUMERIC(10,2),
	Total_promotional_rebates INTEGER,
	Amazon_fees NUMERIC(10,2),
	Other NUMERIC(10,2),
	Total_INR NUMERIC(10,2)
);
