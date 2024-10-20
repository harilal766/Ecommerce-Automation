import platform
from .messages import better_error_handling

def dir_switch(win_dir):
    alternate_dirs = {
        r"D:\6.SPEED POST\1.Shipping labels": r"/home/hari/Desktop/Automation/Test documents/post shipping labels",
        r"D:\5.Amazon\Mathew global\INvoice": r"/home/hari/Desktop/Automation/Test documents/amazon shipping label"
    }
    directory = ""
    try:
        # if pc is win, return win dir
        if platform.system() == 'Windows':
            directory = win_dir
        # if pc is lin, return lin dir
        elif platform.system() == 'Linux':
            directory = alternate_dirs[win_dir]
    except KeyError as e:
        better_error_handling(f"Directory '{win_dir}' not found in alternate_dirs: {e}")
    except Exception as e:
        better_error_handling(e)
    finally:
        return directory



