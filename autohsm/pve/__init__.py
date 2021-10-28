from .base import *


def fire(n=5):
    while True:
        tap(*pos["choose"])
        time.sleep(1)
        tap(*pos["team"])
        time.sleep(0.9)
        tap(*pos["choose"])
        time.sleep(0.4)
        tap(*pos["global_confirm"])

        time.sleep(6)
        tap(*pos["choose"])

        time.sleep(18.5)
        tap(*pos["next_turn"])
        time.sleep(11.5)
        battle()
        time.sleep(22)
        tap(*pos["choose"])
        wait()
        tap(*pos["choose"])
        time.sleep(8)
        get_bonus()
        time.sleep(1.7)

        for _ in range(n - 1):
            if next_node():
                wait()
                tap(*pos["choose"])
                time.sleep(18.5)
                tap(*pos["next_turn"])
                time.sleep(11.5)
                tap(*pos["skill_1"])
                wait()
                tap(*pos["skill_1"])
                wait()
                x, y = pos["skill_0"]
                tap(x, y, x, y - 350, duration=200)
                wait()
                tap(*pos["next_turn"])
                time.sleep(22)
                tap(*pos["choose"])
                wait()
                tap(*pos["choose"])
                time.sleep(8)
                get_bonus()
                time.sleep(1.7)

        while not next_node():
            time.sleep(3)

        quit()
        time.sleep(3)
