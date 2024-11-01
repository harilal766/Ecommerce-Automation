import os
from .messages import better_error_handling

def filepath_constructor(filepath,filename):
    filepath = os.path.join(filepath,filename)
    return filepath


def input_handling(instruction):
    try:
        return instruction
    except KeyboardInterrupt as ki:
        print("Interrupted.")
