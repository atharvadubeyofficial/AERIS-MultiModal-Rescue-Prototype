import numpy as np

from core.sonar import estimate_sonar_clearance
from config.thresholds import SONAR_MIN, SONAR_MAX


def test_estimate_sonar_clearance_bounded():
    frame = np.random.randint(0, 255, (120, 160, 3), dtype=np.uint8)
    clearance = estimate_sonar_clearance(frame, [10, 10, 100, 100])
    assert SONAR_MIN <= clearance <= SONAR_MAX


def test_estimate_sonar_clearance_handles_degenerate_bbox():
    frame = np.zeros((120, 160, 3), dtype=np.uint8)
    clearance = estimate_sonar_clearance(frame, [50, 50, 50, 50])
    assert clearance == 0.50
