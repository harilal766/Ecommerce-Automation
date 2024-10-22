import platform

def dir_switch(directory):
    alternate_dirs = {
        # Post
        "post_label" :(r"D:\6.SPEED POST\1.Shipping labels", r"/home/hari/Desktop/Automation/Test documents/post shipping labels/"),
        # Amazon
        "amazon_label" :(r"D:\5.Amazon\Mathew global\INvoice",r"/home/hari/Desktop/Automation/Test documents/amazon shipping label"),
        "amazon_schedule_report" : (r"",r"")
    }
    if directory not in alternate_dirs:
        raise KeyError(f"Not found.")
    
    if platform.system() == 'Windows':
        return alternate_dirs[directory][0]
    elif platform.system() == 'Linux':
        return alternate_dirs[directory][1]
    else:
        raise OSError("Unsupported OS.")

