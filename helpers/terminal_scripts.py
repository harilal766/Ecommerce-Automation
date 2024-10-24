import os
import time
def clear_terminal():
    print("Clearing Terminal...")
    time.sleep(0.5)
    os.system( 'cls' if os.name == 'nt' else 'clear')


def recompile():
    #compile_status = os.system("C:/Users/USER/AppData/Local/Microsoft/WindowsApps/python3.12.exe d:/Automation/main.py")
    compile_status = os.system("python main.py")
    if compile_status == 0:
        print("Compiled Successfully.")
        clear_terminal()
    else:
        print(f"Compiling failed with Error code : {compile_status}.")
        