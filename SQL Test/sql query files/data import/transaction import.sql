COPY transaction_prepaid(Date, Transaction_type, Order_ID, Product_Details, 
    Total_product_charges, Total_promotional_rebates, Amazon_fees, Other, Total_INR)
FROM 'D:\5.Amazon\Mathew global\Statements\September 27 - Oct 4\prepaid transactions.csv'
DELIMITER ',';


