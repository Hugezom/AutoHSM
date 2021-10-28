from .base import *


def one_turn_fire(n=3):
    print("开始坐牢!")
    i = 0
    while True:
        i += 1
        tap(*pos["choose"])
        time.sleep(1)
        tap(*pos["team"])
        time.sleep(1.5)
        tap(*pos["choose"])
        time.sleep(0.5)
        tap(*pos["global_confirm"])

        time.sleep(5.5)
        tap(*pos["choose"])
        print(f"当前重复次数与位置: {i}-1")

        time.sleep(18.5)
        tap(*pos["next_turn"])
        time.sleep(11.5)
        battle()
        time.sleep(22)
        tap(*pos["choose"])
        wait()
        tap(*pos["choose"])
        time.sleep(10)
        get_bonus()
        time.sleep(1.7)

        for _ in range(n - 1):
            print(f"当前重复次数与位置: {i}-{_+1}")
            if next_node():
                print("Fight!")
                wait()
                tap(*pos["choose"])
                time.sleep(20)
                tap(*pos["next_turn"])
                time.sleep(11.5)
                tap(*pos["skill_1"])
                wait()
                tap(*pos["skill_1"])
                wait()
                x, y = pos["skill_0"]
                tap(x, y, x, y - pos["skill_distance"], duration=200)
                wait()
                tap(*pos["next_turn"])
                time.sleep(22)
                tap(*pos["choose"])
                wait()
                tap(*pos["choose"])
                time.sleep(10)
                get_bonus()
                time.sleep(1.7)

        while not next_node():
            time.sleep(1)

        quit()
        time.sleep(5)

