from config.thresholds import THERMAL_MIN, THERMAL_MAX, THERMAL_CONFIDENCE_GAIN


def estimate_thermal_confirmation(frame, bbox, person_confidence):
    # Software-only placeholder for the physical thermal-camera adapter.
    # Replace this function with actual thermal-frame processing when hardware exists.
    base = THERMAL_MIN + THERMAL_CONFIDENCE_GAIN * person_confidence
    return float(min(THERMAL_MAX, max(THERMAL_MIN, base)))
