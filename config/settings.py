"""App-level (non-scientific) constants for the Streamlit mission-control UI."""

APP_TITLE = "AERIS Mission Control"
APP_ICON = "🚁"
APP_CAPTION = "Perception → Hazard Assessment → Sensor Fusion → Rescue Prioritization"

SCENARIOS = ["Flood Rescue", "Urban Search & Rescue", "Building Emergency"]
VIDEO_FILE_TYPES = ["mp4", "avi", "mov", "mkv"]

FRAME_DELAY_SECONDS = 0.03  # ~30 fps UI refresh cap for the demo loop

SENSOR_STATUS_LABELS = [
    ("🟢", "RGB / YOLO", "REAL"),
    ("🟢", "Hazard estimation", "IMAGE"),
    ("🟡", "Thermal", "SIMULATED"),
    ("🟡", "Sonar", "SIMULATED"),
    ("🟡", "SOS", "SIMULATED"),
]
