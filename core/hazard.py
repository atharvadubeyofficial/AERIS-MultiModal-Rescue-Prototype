import cv2
import numpy as np

from config.thresholds import FLOOD_HSV_LOWER, FLOOD_HSV_UPPER, FLOOD_RATIO_GAIN


def estimate_flood_risk(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array(FLOOD_HSV_LOWER, dtype=np.uint8)
    upper = np.array(FLOOD_HSV_UPPER, dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    ratio = float(np.count_nonzero(mask)) / float(mask.size)
    return float(np.clip(ratio * FLOOD_RATIO_GAIN, 0.0, 1.0))
