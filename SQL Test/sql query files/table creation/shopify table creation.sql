   CREATE TABLE sh_orders (
                        Name VARCHAR(50),
						Email VARCHAR(50),
						Financial_Status VARCHAR(20),
						Paid_at TIMESTAMP,
				        Fulfillment_Status VARCHAR(20),
						Fulfilled_at TIMESTAMP,
						Accepts_Marketing BOOLEAN,
						Currency VARCHAR(50),
				        Subtotal NUMERIC(10,2), 
						Shipping NUMERIC(10,2),   
						Taxes NUMERIC(10,2),    
						Total NUMERIC(10,2),
        Discount_Code VARCHAR(50),  
		Discount_Amount NUMERIC(10,2),        
		Shipping_Method VARCHAR(50),    
		Created_at TIMESTAMP,
		
        Lineitem_quantity NUMERIC(10,2),        
		Lineitem_name VARCHAR(50),      
		Lineitem_price NUMERIC(10,2),   
		Lineitem_compare_at_price NUMERIC(10,2),
        Lineitem_sku VARCHAR(50),       
		Lineitem_requires_shipping VARCHAR(50), 
		Lineitem_taxable VARCHAR(50),   
		Lineitem_fulfillment_status VARCHAR(20),
		
        Billing_Name VARCHAR(50),       
		Billing_Street VARCHAR(50),     
		Billing_Address1 VARCHAR(100),  
		Billing_Address2 VARCHAR(100),
        Billing_Company VARCHAR(50),    
		Billing_City VARCHAR(100),      
		Billing_Zip CHAR(8),    
		Billing_Province VARCHAR(50),
        Billing_Country VARCHAR(50),    
		Billing_Phone VARCHAR(15),  
		
		Shipping_Name VARCHAR(50),      
		Shipping_Street VARCHAR(50),
        Shipping_Address1 VARCHAR(100), 
		Shipping_Address2 VARCHAR(100), 
		Shipping_Company VARCHAR(50),   
		Shipping_City VARCHAR(100),
        Shipping_Zip CHAR(8),   
		Shipping_Province VARCHAR(50),  
		Shipping_Country VARCHAR(50),   
		Shipping_Phone VARCHAR(15),
		
        Notes VARCHAR(50),      
		Note_Attributes VARCHAR(100),      
		
		Cancelled_at TIMESTAMP, 
		
		Payment_Method VARCHAR(50),
        Payment_Reference VARCHAR(50),  
		
		Refunded_Amount NUMERIC(10,2),  
		Vendor VARCHAR(50),     
		Outstanding_Balance NUMERIC(10,2),
        Employee VARCHAR(50),   
		
		Location VARCHAR(50),     
		Device_ID VARCHAR(20),  
		Id VARCHAR(20),
        Tags VARCHAR(100),       
		
		Risk_Level VARCHAR(50),     Source VARCHAR(50),     Lineitem_discount NUMERIC(10,2),
		
        Tax_1_Name VARCHAR(50), Tax_1_Value VARCHAR(50),        Tax_2_Name VARCHAR(50), Tax_2_Value VARCHAR(50),
        Tax_3_Name VARCHAR(50), Tax_3_Value VARCHAR(50),        Tax_4_Name VARCHAR(50), Tax_4_Value VARCHAR(50),
        Tax_5_Name VARCHAR(50), Tax_5_Value VARCHAR(50),        
		
		Phone VARCHAR(15),      Receipt_Number NUMERIC(10,2),
        Duties VARCHAR(50),     
		
		Billing_Province_Name VARCHAR(50),      Shipping_Province_Name VARCHAR(50),     Payment_ID VARCHAR(50),
        Payment_Terms_Name VARCHAR(50), Next_Payment_Due_At TIMESTAMP,  Payment_References VARCHAR(50)
            );