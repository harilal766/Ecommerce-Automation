
copy Orders (
	amazon_order_id, merchant_order_id, purchase_date, last_updated_date, order_status, fulfillment_channel, sales_channel, order_channel, url, ship_service_level, product_name, sku, asin, item_status, quantity, currency, item_price, item_tax, shipping_price, shipping_tax, gift_wrap_price, gift_wrap_tax, item_promotion_discount, ship_promotion_discount, ship_city, ship_state, ship_postal_code, ship_country, promotion_ids, is_business_order, purchase_order_number, price_designation, is_iba
	) 
FROM 'D:/Automation/SQL Test/Order table txt/Orders 1.10.24 - 7.10.24.txt' 
WITH (
	FORMAT text,
	DELIMITER E'\t',
	ENCODING 'UTF8',
	NULL 'null'
);


