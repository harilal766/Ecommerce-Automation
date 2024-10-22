import os
import time
def clear_terminal():
    print("Clearing Terminal...")
    time.sleep(0.5)
    os.system( 'cls' if os.name == 'nt' else 'clear')
        