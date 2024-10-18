from loguru import logger
from colorama import Fore,Style,init


init()

def better_error_msg(error):
    """
    Establish a boundary
    Error heading
    Mesaage printing
    End of boundary
        """
    boundary = f"\033[31m {'-'*90} \033[0m"
    print(boundary)
    logger.exception(error)
    print(boundary)


def success_status_msg(status):
    print(Fore.GREEN+status+Style.RESET_ALL)
    
