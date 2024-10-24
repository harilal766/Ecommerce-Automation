import time

def loading_animation(value):
    loading_dot = "."
    if value != 0:
        print("Loading",end="")
        for i in range(5):
            time.sleep(0.2)
            print(loading_dot,end="")
    else:
        pass

loading_animation(5)