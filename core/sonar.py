import cv2
import numpy as np

from config.thresholds import SONAR_BASELINE, SONAR_TEXTURE_GAIN, SONAR_MIN, SONAR_MAX


def estimate_sonar_clearance(frame, bbox):
    # Software-only placeholder for physical sonar/range sensor integration.
    x1, y1, x2, y2 = bbox
    h, w = frame.shape[:2]
    x1 = max(0, min(w - 1, x1)); x2 = max(0, min(w, x2))
    y1 = max(0, min(h - 1, y1)); y2 = max(0, min(h, y2))
    if x2 <= x1 or y2 <= y1:
        return 0.50
    crop = frame[y1:y2, x1:x2]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    texture = float(np.std(gray)) / 128.0
    return float(np.clip(SONAR_BASELINE + texture * SONAR_TEXTURE_GAIN, SONAR_MIN, SONAR_MAX))
