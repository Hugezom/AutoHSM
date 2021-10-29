from ..utils import *
import yaml

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
tpl_red_up = cv2.imread(f"configs/{device}/templates/red_up.png")
tpl_blue_up = cv2.imread(f"configs/{device}/templates/blue_up.png")


def battle():
    tap(*pos["skill_1"])
    wait()
    tap(*pos["skill_1"])
    wait()
    x, y = pos["skill_0"]
    tap(x, y, x, y - 350, duration=200)


def get_bonus():
    tap(*pos["skill_0"])
    time.sleep(0.5)
    tap(*pos["bonus_confirm"])


def get_buff(img, threshold=0.9, _x=0, _y=0):
    for tpl in [tpl_red_up, tpl_blue_up]:
        result = cv2.matchTemplate(img, tpl, cv2.TM_CCOEFF_NORMED)
        confidence = result.max()
        if confidence >= threshold:
            _a, _b = tpl.shape[:2]
            b, a = divmod(np.argmax(result), result.shape[1])

            a = int(a + _a / 2 + _y)
            b = int(b + _b / 2 + _x)

            print(f"Find buff, confidence {confidence}")
            tap(a, b)
            time.sleep(0.3)
            tap(*pos["choose"])
            tap(*pos["global_confirm"])
            time.sleep(1)
            return True
    return False


def get_angle(img, threshold=0.9, _x=0, _y=0):
    result = cv2.matchTemplate(img, tpl_angle, cv2.TM_CCOEFF_NORMED)
    confidence = result.max()
    if confidence >= threshold:
        _a, _b = tpl_angle.shape[:2]
        b, a = divmod(np.argmax(result), result.shape[1])

        a = int(a + _a / 2 + _y)
        b = int(b + _b / 2 + _x)

        print(f"Find angle, confidence {confidence}")
        tap(a, b)
        time.sleep(0.3)
        tap(*pos["choose"])
        time.sleep(2)
        return True
    else:
        return False


def get_mystery(img, threshold=0.9, _x=0, _y=0):
    result = cv2.matchTemplate(img, tpl_mystery, cv2.TM_CCOEFF_NORMED)
    confidence = result.max()
    if confidence >= threshold:
        _a, _b = tpl_mystery.shape[:2]
        b, a = divmod(np.argmax(result), result.shape[1])

        a = int(a + _a / 2 + _x)
        b = int(b + _b / 2 + _y)

        print(f"Find mystery, confidence {confidence}")
        tap(a, b)
        time.sleep(0.3)
        tap(*pos["choose"])
        time.sleep(0.5)
        tap(*pos["skill_1"])
        time.sleep(1)
        tap(*pos["mystery_confirm"])
        wait()
        tap(*pos["mystery_confirm"])
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
        get_mystery(img, _x=x_range[0], _y=y_range[0], threshold=0.95)
        or get_angle(img, _x=x_range[0], _y=y_range[0], threshold=0.95)
        or get_buff(img, _x=x_range[0], _y=y_range[0], threshold=0.95)
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

        if circles is None:
            e = TypeError("没有检测到圆. 查看是否处于地图界面!")
            print(e)
            return e

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
    time.sleep(0.5)
    tap(*pos["next_turn"])


def quit():
    tap(*pos["check_team"])
    wait()
    tap(*pos["give_up"])
    wait()
    tap(*pos["global_confirm"])
    wait(1.5)
    tap(*pos["global_confirm"])
    wait()
    tap(*pos["global_confirm"])


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
