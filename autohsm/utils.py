import os
import cv2
import time
import random
import numpy as np
import subprocess


def detect_device():
    devices = os.popen("adb devices").read().split("\n")[1]
    if devices == "":
        raise IOError("There is no device detected!")
    else:
        device = devices.split("\t")[0]
        print(f"Device {device} detected!")
        return device


def tap(x, y, tx=None, ty=None, error=15, duration: int = 0):
    x += random.uniform(-error, error)
    y += random.uniform(-error, error)
    duration += int(random.uniform(50, 80))
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
    pipe = subprocess.Popen(
        "adb shell screencap -p",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True,
    )
    image_bytes = pipe.stdout.read().replace(b"\r\n", b"\n")
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    return image

