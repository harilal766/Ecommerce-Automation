import os,sys,subprocess
import time
from helpers.messages import better_error_handling,color_print
def clear_terminal():
    print("Clearing Terminal...")
    time.sleep(0.5)
    os.system( 'cls' if os.name == 'nt' else 'clear')

def recompile():
    try:
        #python_path = str(sys.executable)
        python_path = r"C:/Program Files/Python313/python.exe"
        script_path = r"d:/Ecommerce-Automation/main.py"
        command = f'"{python_path}" "{script_path}"'
        color_print(message=python_path,color='blue')
        color_print(message="Recompiling....",color='blue')
        clear_terminal()
        subprocess.run(command, check=True) 
    except Exception as e:
        better_error_handling(e)

        




def bedtime_reminder(): 
    # 
    pass
    
        