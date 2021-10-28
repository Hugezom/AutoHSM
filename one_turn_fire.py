from autohsm.pve import one_turn_fire
import argparse


parser = argparse.ArgumentParser(description="火焰队坐牢")
parser.add_argument("--n", "-n", help="坐牢层数, 默认为4", default=4)
args = parser.parse_args()

if __name__ == "__main__":
    try:
        one_turn_fire(args.n)
    except Exception as e:
        print(e)
