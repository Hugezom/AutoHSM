import os
import cv2
import time
import yaml
import random
import numpy as np
import subprocess

def init():
    global pos, tpl_start, tpl_surrender, tpl_matching
    device = detect_device()
    if not os.path.exists(f"configs/{device}/"):
        raise IOError("Cannot find configuration for device {device}! Please create a folder like `configs/example/` in `configs/`.")

    with open(f"configs/{device}/position.yaml") as f:
        pos = yaml.safe_load(f)

    tpl_start = cv2.imread(f"configs/{device}/templates/start.png")
    tpl_surrender = cv2.imread(f"configs/{device}/templates/surrender.png")
    tpl_matching = cv2.imread(f"configs/{device}/templates/matching.png") 

def detect_device():
    devices = os.popen("adb devices").read().split('\n')[1]
    if devices == "":
        raise IOError("No device detected!")
    else:
        device = devices.split('\t')[0]
        return device

def tap(x, y, tx=None, ty=None, error=15, duration: int = 0):
    x += random.uniform(-error, error)
    y += random.uniform(-error, error)
    duration += int(random.uniform(50, 100))
    if tx is None:
        tx = x
    tx += random.uniform(-error, error)
    if ty is None:
        ty = y
    ty += random.uniform(-error, error)
    os.system(f"adb shell input swipe {x} {y} {tx} {ty} {duration}")


def wait(t=0.2):
    error = random.uniform(0, 0.2)
    time.sleep(t + error)

def catch_screen():
    pipe = subprocess.Popen("adb shell screencap -p",
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            shell=True)
    image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8),
                         cv2.IMREAD_COLOR)
    return image

def surrender(t, threshold=0.9):
    tap(*pos["setting"])
    time.sleep(0.5)
    screen = catch_screen()
    result = cv2.matchTemplate(screen, tpl_surrender, cv2.TM_CCOEFF_NORMED)
    if result.max() >= threshold:
        time.sleep(t)
        tap(*pos["surrender"])
    else:
        tap(*pos["choose"])
    time.sleep(0.2)
    tap(*pos["choose"])
    wait()
    tap(*pos["choose"])
    wait()
    tap(*pos["choose"])

def check_start(img, threshold=0.9, has_error=False):
    if has_error:
        result = cv2.matchTemplate(img, tpl_error, cv2.TM_CCOEFF_NORMED)
        if result.max()>=threshold:
            tap(*pos["error_confirm"])
    
    result = cv2.matchTemplate(img, tpl_start, cv2.TM_CCOEFF_NORMED)
    should_start = result.max() >= threshold
    if should_start:
        tap(*pos["choose"])

        wait(0.3)
        tap(*pos["team"])

        wait()
        tap(*pos["choose"])
    return should_start

def is_matching(img, threshold=0.9):
    return cv2.matchTemplate(img, tpl_matching,
                             cv2.TM_CCOEFF_NORMED).max() >= threshold