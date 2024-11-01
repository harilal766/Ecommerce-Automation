select s.name as order_id,t.Barcode,s.fulfilled_at,s.Lineitem_name,s.Lineitem_quantity as product_qty,s.Lineitem_price as price,s.Lineitem_compare_at_price as compare, s.Billing_Province as state,
	pc.Quantity as order_qty,pc.Weight,pc.Door_delivery_amount,pc.POD_amount,pc.Line_Item___Total_Amount,pc.Tax_Amount 
	from 
		sh_orders s join tj_cod t on s.name = t.REF
		JOIN po_cod pc on t.Barcode = pc."Tracking_ID_/_Article_ID";