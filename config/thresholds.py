"""
Central place for every tunable number in the AERIS decision pipeline.

Judges will ask "why these weights?" — keep this file as the single
source of truth so the answer is always "see config/thresholds.py",
and so weights can be re-tuned without touching pipeline logic.
"""

# ---- Sensor-fusion weights (must sum to 1.0) --------------------------
FUSION_WEIGHTS = {
    "person_confidence": 0.30,  # RGB / YOLO detection confidence
    "thermal_confidence": 0.25,  # thermal confirmation (simulated in prototype)
    "flood_risk": 0.20,          # environmental hazard around the target
    "sonar_clearance": 0.15,     # approach-path clearance (simulated in prototype)
    "sos": 0.10,                 # active SOS / LoRa beacon (simulated in prototype)
}

assert abs(sum(FUSION_WEIGHTS.values()) - 1.0) < 1e-6, "FUSION_WEIGHTS must sum to 1.0"

# ---- Rescue-priority bands (fusion score is 0-100) ---------------------
PRIORITY_BANDS = {
    "CRITICAL": 75.0,
    "HIGH": 55.0,
    "MEDIUM": 35.0,
    "LOW": 0.0,
}

PRIORITY_ORDER = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}

# ---- Perception defaults ------------------------------------------------
DEFAULT_PERSON_CONFIDENCE = 0.35
DEFAULT_MAX_TARGETS = 5
YOLO_MODEL_NAME = "yolo11n.pt"  # nano model: runs on CPU, good for live demo

# ---- Hazard (flood) estimation ------------------------------------------
# HSV range used to approximate standing/flowing water in a video frame.
FLOOD_HSV_LOWER = (80, 35, 35)
FLOOD_HSV_UPPER = (135, 255, 255)
FLOOD_RATIO_GAIN = 3.0  # scales raw pixel ratio into a 0-1 risk score

# ---- Sonar (simulated) ----------------------------------------------------
SONAR_BASELINE = 0.45
SONAR_TEXTURE_GAIN = 0.25
SONAR_MIN = 0.35
SONAR_MAX = 0.85

# ---- Thermal (simulated) --------------------------------------------------
THERMAL_MIN = 0.55
THERMAL_MAX = 0.95
THERMAL_CONFIDENCE_GAIN = 0.40

# ---- SOS (simulated demo event) -------------------------------------------
SOS_TRIGGER_FRAME = 60
