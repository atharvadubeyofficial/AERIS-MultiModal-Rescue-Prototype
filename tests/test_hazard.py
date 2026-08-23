import numpy as np

from core.hazard import estimate_flood_risk


def test_estimate_flood_risk_returns_bounded_value():
    frame = np.random.randint(0, 255, (120, 160, 3), dtype=np.uint8)
    risk = estimate_flood_risk(frame)
    assert 0.0 <= risk <= 1.0


def test_estimate_flood_risk_high_for_blue_frame():
    frame = np.zeros((120, 160, 3), dtype=np.uint8)
    frame[:, :, 0] = 200  # BGR: strong blue channel -> should read as watery
    risk = estimate_flood_risk(frame)
    assert risk > 0.3
