from report_generator import amazon_shipment_report
from scripts.postal_tracking import postal_track
import os
# Menu
feature_menu = {
    1:("Amazon shipment report", amazon_shipment_report),
    2:("Shopify shipment report",""),
    3:("Post Tracking",postal_track),
    4:("Delete duplicate csv files","")
}
# Split into 2 menu dictionaries
feat_last_key = list(feature_menu.keys())[-1]
exit_menu = {
    feat_last_key+1:("Exit",postal_track),
    feat_last_key+2:("Developer Settings","")
    }

menu = {**feature_menu, **exit_menu}

space = "-"*15

while True:
    # Prompting the user for an option
    print(f"{space}MENU{space}")
    for option in menu:
        print(f"{option}. {menu[option][0]}")
    print(f"{space}-----{space}")
    try:
        selection = int(input("Select an option : "))
    except ValueError:
        print("Please enter a number")
        continue

    # Processing the selected input
    if (selection in menu):
        if selection == max(menu.keys()):
            print("Exiting The Program")
            break
        else:
            print(f"You have selected {menu[selection][0]}")
            menu[selection][1]()
            # Clearing the terminal after every selection
            os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print("Invalid Selection,Try again.")