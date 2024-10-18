import itertools
import time
import sys


def loading_animation(duration):
    rotating = [".",".",".",".","."]
    runtime = time.time()
    print("Loading",end="")
    for frame in itertools.cycle(rotating):
        sys.stdout.write(f"{frame}")
        sys.stdout.flush()
        time.sleep(0.2)

        if (time.time() - runtime) > duration:
            break
    print()
    
