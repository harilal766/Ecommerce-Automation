from loguru import logger
from colorama import Fore,Style,init
import shutil

init()
terminal_width = shutil.get_terminal_size()
print(terminal_width)
hyphen = "-"* 90
red_boundary = ""


green_boundary = f"{Fore.GREEN}{hyphen}{Style.RESET_ALL}"
def better_error_handling(error):
    exc_and_clarifications = {
        FileNotFoundError : "File/Directory Not Found"
    }
    """
    Establish a boundary
    Error heading
    Mesaage printing
    End of boundary
        """
    boundary = f"\033[31m {hyphen} \033[0m"
    print(boundary)
    logger.exception(exc_and_clarifications[error])
    print(boundary)


def success_status_msg(status):
    print(green_boundary)
    print(f"{Fore.GREEN}{status}{Style.RESET_ALL}")
    print(green_boundary)
    

