select * from sh_orders where name in (select name from sh_orders where Financial_status = "pending") 
	order by name asc;