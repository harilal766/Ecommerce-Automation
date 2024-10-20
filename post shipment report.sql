
            SELECT DISTINCT
            Name, Email, Financial_Status, Paid_at, Fulfillment_Status, Fulfilled_at, Subtotal, Shipping, Total, Lineitem_quantity, Lineitem_name, Lineitem_price, Lineitem_compare_at_price, Billing_Name, Billing_Street, Billing_Address1, Billing_Address2, Billing_Company, Billing_City, Billing_Zip, Billing_Province, Billing_Country, Billing_Phone, Shipping_Name, Shipping_Street, Shipping_Address1, Shipping_Address2, Shipping_Company, Shipping_City, Shipping_Zip, Shipping_Province, Shipping_Country, Shipping_Phone, Location, Device_ID, Id, Tags, Lineitem_discount, Billing_Province_Name, Shipping_Province_Name, 
            FROM sh_orders 
            WHERE name IN (
                	'#12923','#12924','#12928',
'#12929','#12935','#12936',
'#12939','#12942','#12943',
'#12944','#12945','#12945'
            )
            ORDER BY lineitem_name ASC, lineitem_price ASC;
        