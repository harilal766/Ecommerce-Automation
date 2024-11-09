from helpers.file_ops import *
from helpers.sql_scripts import query_backup,line_limit_checker,sql_to_excel,db_connection,sql_table_creation_or_updation
from helpers.loading_animations import loading_animation
from helpers.regex_patterns import *
"""
    make the query for filtering orders form sql table bsaed on seperate cod and non cod pdf files
"""



def filter_query(pdf_path,pattern,fields,database,table,id,order_by_clause,
                    sql_filename,
                    input_filepath,out_excel_path):
    function_boundary(title="FILTERING QUERY")
    order_ids = None
    order_id_list = pdf_pattern_finder(message="Enter the pdf filename with extension : ",filepath=pdf_path,pattern=pattern)
    #last_column = order_id_list[-1]
    try:
        order_ids = ""; order_id_count = 0
        for order_id in order_id_list:
            order_id_count+=1
            if order_id_list[-1] == order_id:
                order_ids+= f"'{order_id}'"
            elif line_limit_checker(word_count=order_id_count,line_limit=3):
                order_ids+= f"'{order_id}',\n"
            elif not line_limit_checker(word_count=order_id_count,line_limit=3):
                order_ids+= f"'{order_id}',"

            
            # avoiding the comma from the last column
        # Strip comma from last order id by identifying it using the pattern
        shipment_report_query = f"""
            SELECT DISTINCT
            {fields} 
            FROM {table} 
            WHERE {id} IN (
                \t{order_ids}
            )
            ORDER BY {order_by_clause};
        """
        #loading_animation(len(order_ids)), ask for the loading value and execute the loading animation only while it is not executed. 
        
        # Backing up the query
        query_backup(f"{sql_filename}",shipment_report_query)

        # Creating the table and closing
        sql_table_creation_or_updation(dbname=database,tablename=table,
                                       replace_or_append="replace",
                                       input_file_dir=input_filepath)
        
        # connecting to the db
        connection = db_connection(dbname=database,db_system="sqlite")
        if connection:
            success_status_msg("Connection Succeeded.")
            cursor = connection.cursor()
            cursor.execute(shipment_report_query)
            results = cursor.fetchall()
            # converting the sql result into excel file
            sql_to_excel(sql_cursor=cursor,query_result=results,out_excel_path=out_excel_path)
        else:
            status_message(message="Connection Failed",color="red")
        
    except Exception as e:
        better_error_handling(e)
    finally:
        success_status_msg(shipment_report_query)
        # closing the db
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and connection:
            connection.close()



def table_querying(operation):
    pass



# Driver code for report generator
def report_driver(report_type): 
    report_type = report_type.lower()
    if "amazon" in report_type:
        filter_query(
            #pdf_path="/home/hari/Desktop/Automation/Test documents/amazon shipping label",
            pdf_path=dir_switch(win=win_amazon_invoice,lin=lin_amazon_invoice),
            pattern=amazon_order_id_pattern,
            fields="""amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax""",
            database="Amazon",table="Orders", id = "amazon_order_id",
            order_by_clause="product_name asc,quantity asc",
            sql_filename="amzn_shipment_query",
            input_filepath=dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report),
            out_excel_path=dir_switch(win=win_amazon_scheduled_report,lin=lin_amazon_scheduled_report)
        )
    elif "shopify" in report_type:
        filter_query(
            #pdf_path="/home/hari/Desktop/Automation/Test documents/post shipping labes",
            pdf_path=dir_switch(win=win_shopify_invoice,lin=lin_shopify_invoice),
            pattern=post_order_id_pattern,
            fields=""" Name, Financial_Status, Paid_at, Fulfillment_Status, Fulfilled_at, Subtotal, Shipping, Total, Lineitem_quantity, Lineitem_name,Lineitem_price, Lineitem_compare_at_price, Shipping_Province_Name""",
            database="Shopify",table="sh_orders",id="name",
            order_by_clause="lineitem_name ASC, lineitem_price ASC",
            sql_filename="post shipment report query",
            input_filepath=dir_switch(win=win_shopify_order_excel_file,lin=lin_shopify_order_excel_file),
            out_excel_path=dir_switch(win=win_shopify_order_excel_file,lin=lin_shopify_order_excel_file)
        )