from ..utils import *


device = detect_device()
if not os.path.exists(f"configs/{device}/"):
    raise IOError(
        "Cannot find configuration for device {device}! Please create a folder like `configs/example/` in `configs/`."
    )

with open(f"configs/{device}/position.yaml") as f:
    pos = yaml.safe_load(f)

tpl_mystery = cv2.imread(f"configs/{device}/templates/mystery.png")
tpl_angle = cv2.imread(f"configs/{device}/templates/angle.png")
tpl_up = cv2.imread(f"configs/{device}/templates/up.png")


def battle():
    tap(*pos["skill_1"])
    wait()
    tap(*pos["skill_1"])
    wait()
    x, y = pos["skill_0"]
    tap(x, y, x, y - 350, duration=200)


def get_bonus():
    tap(*pos["skill_0"])
    wait()
    tap(*pos["bonus_confirm"])


def get_buff(img, tpl, threshold=0.9, _x=0, _y=0):
    result = cv2.matchTemplate(img, tpl, cv2.TM_CCOEFF_NORMED)
    if result.max() >= threshold:
        _a, _b = tpl_angle.shape[:2]
        b, a = divmod(np.argmax(result), result.shape[1])

        a = int(a + _a / 2 + _y)
        b = int(b + _b / 2 + _x)

        tap(a, b)
        wait()
        tap(*pos["choose"])
        time.sleep(0.5)
        tap(*pos["global_confirm"])
        return True
    else:
        return False


def get_mystery(img, threshold=0.9, _x=0, _y=0):
    result = cv2.matchTemplate(img, tpl_mystery, cv2.TM_CCOEFF_NORMED)
    if result.max() >= threshold:
        _a, _b = tpl_angle.shape[:2]
        b, a = divmod(np.argmax(result), result.shape[1])

        a = int(a + _a / 2 + _x)
        b = int(b + _b / 2 + _y)

        tap(a, b)
        wait()
        tap(*pos["choose"])
        wait()
        tap(*pos["skill_1"])
        wait()
        tap(*pos["mystery_confirm"])
        wait()
        tap(*pos["choose"])
        return True
    else:
        return False


def next_node():
    img = catch_screen()
    a, b, _ = img.shape
    x_range = int(0.25 * a), int(0.7 * a)
    y_range = int(0.1 * b), int(0.7 * b)
    img = img[x_range[0] : x_range[1], y_range[0] : y_range[1]]

    if (
        get_buff(img, tpl_mystery, _x=x_range[0], _y=y_range[0])
        or get_buff(img, tpl_angle, _x=x_range[0], _y=y_range[0])
        or get_buff(img, tpl_up, _x=x_range[0], _y=y_range[0], threshold=0.95) #容易误识别
    ):
        return False

    else:

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY,)
        circles = cv2.HoughCircles(
            img,
            cv2.HOUGH_GRADIENT,
            1,
            a / 20,
            param1=100,
            param2=70,
            minRadius=int(a / 18),
            maxRadius=int(a / 12),
        )
        circles = np.int0(np.around(circles))

        for i in circles[0]:
            tap(i[0] + y_range[0], i[1] + x_range[0])
        return True


def battle():
    tap(*pos["skill_1"])
    wait()
    tap(*pos["skill_1"])
    wait()
    x, y = pos["skill_0"]
    tap(x, y, x, y - 350, duration=200)
    wait()
    tap(*pos["next_turn"])


def quit():
    tap(*pos["check_team"])
    wait()
    tap(*pos["give_up"])
    wait()
    tap(*pos["global_confirm"])
    wait(1.5)
    tap(*pos["choose"])
