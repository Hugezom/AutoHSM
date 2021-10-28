from .base import *
from ..pvp.base import surrender


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

        has_error = False
        for _ in range(n - 1):
            print(f"当前重复次数与位置: {i}-{_+2}")
            nd = next_node()
            if nd is True:
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
                tap(x, y, x, y - 350, duration=200)
                wait()
                tap(*pos["next_turn"])
                time.sleep(22)
                tap(*pos["choose"])
                wait()
                tap(*pos["choose"])
                time.sleep(10)
                get_bonus()
                time.sleep(1.7)

            elif isinstance(nd, TypeError):
                has_error = True
                print("尝试自救!")
                surrender()
                time.sleep(2)
                tap(*pos["global_confirm"])
                wait()
                tap(*pos["global_confirm"])
                break

        while not has_error and not next_node():
            time.sleep(1)

        quit()
        time.sleep(5)
