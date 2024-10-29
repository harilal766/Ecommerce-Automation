import os

def filepath_constructor(filepath,filename):
    filepath = os.path.join(filepath,filename)
    return filepath