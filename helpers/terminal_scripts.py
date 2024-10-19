import os
import platform

def clear_terminal():
    if platform == "Linux":
        os.system("clear && history -c && history -w")
    elif platform == "Windows":
        os.system('ctrl + l')



import urwid

def exit_program(key):
    if key == 'q':
        raise urwid.ExitMainLoop()


