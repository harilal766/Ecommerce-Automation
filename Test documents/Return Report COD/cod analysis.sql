SELECT 
    s.name AS order_id,
    t.Barcode,
    s.fulfilled_at,
    s.Lineitem_name,
    s.Lineitem_price AS price,
    s.Lineitem_quantity AS product_qty,
    s.Shipping ,
    s.Billing_Province AS state
FROM 
    sh_orders s
JOIN 
    tj_cod t ON s.name = t.REF
JOIN
	po_cod pc ON t.Barcode = pc.Assignment
WHERE s.Lineitem_name != "COD-Fees"
ORDER BY "Assignment" ASC
;
