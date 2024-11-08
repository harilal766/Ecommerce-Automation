from report_generator import report_driver
from scripts.postal_tracking import postal_track
from helpers.terminal_scripts import clear_terminal,recompile
from helpers.sql_scripts import order_table_updation
from helpers.file_ops import function_boundary
from datetime import datetime, timedelta, timezone
from api_driver import amazon_api_driver
# Menu
feature_menu = {
    0:("Clear Terminal",clear_terminal),
    1:("Amazon shipment report", report_driver),
    2:("Shopify shipment report",report_driver),
    4:("Table updation",order_table_updation),
    5:("Orders API",amazon_api_driver),
    6:("Order API",amazon_api_driver),
    7:("Amazon Report API",amazon_api_driver)
}
# Split into 2 menu dictionaries
feat_last_key = list(feature_menu.keys())[-1]
exit_menu = {
    feat_last_key+1:("Recompile",recompile)
    }

menu = {**feature_menu, **exit_menu}
space = "-"*15

def main():
    while True:
        # Prompting the user for an option
        function_boundary(title="MENU")
        for option in menu:
            print(f"{option}. {menu[option][0]}")
        print(f"{space}-----{space}")
        try:
            selection = int(input("Select an option : "))
        except ValueError:
            print("Please enter a number\n")
            continue
        except KeyboardInterrupt:
            print("No option selected.\n")
            continue

        # Processing the selected input
        if (selection in menu):
            print(f"You have selected : {menu[selection][0]}")
            argument = menu[selection][0].lower()
            # selectin api and report functions
            if "report" in argument or "api" in argument:
                menu[selection][1](argument)
            else:
                menu[selection][1]()
        else:
            print("Invalid Selection,Try again.")

            
if __name__ == "__main__":
    main()