import os, datetime

def target_file(dd,mm,yy,folder):
    if mm[0]=="0":
        mm=mm[1]
    if dd[0]=="0":
        dd=dd[1]
    main = folder.split(".")[-1]; target= ""
    if main == "Amazon":
        target = f'scheduled for {dd}.{mm}.{yy[2:4]}-COD.xlsx' and f'scheduled for {dd}.{mm}.{yy[2:4]}.xlsx'
    elif main == "Shopify":
        target = f"{dd}.{mm}.{yy[2:4]}.xlsx"
    return target

def dir(directory):
    results = os.listdir(directory)
    today=str(datetime.datetime.today()).split(" ")[0]
    year = today[0:4]; month = today[5:7]; day = today[8:11]
    main_folder = directory.split("\\")[1]
    sub_folder = directory.split("\\")[-1]
    folder = main_folder +" "+ sub_folder
    ##print(f"{file} - {target_file(day,month,year)} - {target_file(day,month,year) in results}")
    print(f"|{folder} | {target_file(day,month,year,main_folder)} | {target_file(day,month,year,folder) in results}|")
    
    
dir(r'D:\5.Amazon\Mathew global\Scheduled report')
dir(r"D:\3.Shopify\Date wise order list")



    
