from ..utils import *
import yaml

device = detect_device()
if not os.path.exists(f"configs/{device}/"):
    raise IOError(
        "Cannot find configuration for device {device}! Please create a folder like `configs/example/` in `configs/`."
    )

with open(f"configs/{device}/position.yaml") as f:
    pos = yaml.safe_load(f)

tpl_start = cv2.imread(f"configs/{device}/templates/start.png")
tpl_surrender = cv2.imread(f"configs/{device}/templates/surrender.png")
tpl_matching = cv2.imread(f"configs/{device}/templates/matching.png")


def start():
    tap(*pos["choose"])

    wait(0.3)
    tap(*pos["team"])

    wait()
    tap(*pos["choose"])


def check_start(img, threshold=0.9):
    result = cv2.matchTemplate(img, tpl_start, cv2.TM_CCOEFF_NORMED)
    should_start = result.max() >= threshold
    if should_start:
        start()
    return should_start


def is_matching(img, threshold=0.9):
    return cv2.matchTemplate(img, tpl_matching, cv2.TM_CCOEFF_NORMED).max() >= threshold


def surrender(t=0, threshold=0.9):
    tap(*pos["setting"])
    time.sleep(0.2)
    # screen = catch_screen()
    # result = cv2.matchTemplate(screen, tpl_surrender, cv2.TM_CCOEFF_NORMED)
    # if result.max() >= threshold:
    #    time.sleep(t)
    #    tap(*pos["surrender"])
    # else:
    #    tap(*pos["choose"])
    time.sleep(t)
    tap(*pos["surrender"])
    time.sleep(0.2)
    tap(*pos["setting"])
    time.sleep(0.2)
    tap(*pos["choose"])
    time.sleep(0.2)
    tap(*pos["choose"])
