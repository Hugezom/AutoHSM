from .utils import *
import os
import yaml

def main(wait_seconds=0):
    init()
    print("Start to surrender!")

    should_run = True
    while should_run:
        screen = catch_screen()
        if check_start(screen):
            time.sleep(0.3)
            screen = catch_screen()
            
        while is_matching(screen):
            time.sleep(1)
            screen = catch_screen()
        wait(3.3)
        surrender(wait_seconds)
        
        wait(3.1)
        #check_rewards(screen)