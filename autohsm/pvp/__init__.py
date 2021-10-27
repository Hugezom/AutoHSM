import time
from ._surrender import *

def surrender(wait_seconds=0, check_interval=0.3):
    init()
    print("Start to surrender!")

    should_run = True
    while should_run:
        #screen = catch_screen()
        #if check_start(screen):
        #    time.sleep(check_interval)
        #    screen = catch_screen()
        start()
        time.sleep(0.3)

        while is_matching(catch_screen()):
            time.sleep(check_interval)

        time.sleep(1)
        surrender(wait_seconds)
        
        time.sleep(2)
        #check_rewards(screen)