from loguru import logger
from colorama import Fore,Style,init
import shutil
import re

init()
terminal_width = shutil.get_terminal_size()
print(terminal_width)
hyphen = "-"* 110
red_boundary = ""


green_boundary = f"{Fore.GREEN}{hyphen}{Style.RESET_ALL}"
def better_error_handling(error):

    exceptions = {
        # File related errors
        FileNotFoundError : "The file not found on the directory",
        # Import related
        ImportError : "The libraries you tried to import does not exist"
    }
    """
    Establish a boundary
    Error heading
    Mesaage printing
    End of boundary
        """
    boundary = f"\033[31m {hyphen} \033[0m"
    print(boundary)
    logger.exception(f"\n{exceptions[error]}" if error in exceptions else f"Error : {error}")
    print(boundary)


def success_status_msg(status):
    #print(green_boundary)
    print(f"{Fore.GREEN}{status}{Style.RESET_ALL}")
    #print(green_boundary)

def status_message(message,color):
    foregreen = None
    if color.lower() == 'red':
        foregreen = Fore.RED
    elif color.lower() == 'green':
        foregreen = Fore.GREEN
    elif color.lower() == "blue":
        foregreen = Fore.BLUE
    if message[-1] == r'\w':
        message = message +'.'
    print(f"{foregreen}{message}{Style.RESET_ALL}")
        
