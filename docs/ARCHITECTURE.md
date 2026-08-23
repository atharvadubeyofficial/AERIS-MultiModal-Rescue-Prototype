# AERIS Architecture

UAV/Camera
→ Video Source
→ RGB AI Perception
→ Thermal / Hazard / Sonar interfaces
→ Sensor Fusion
→ Rescue Priority
→ Mission Planner
→ Mission Control

Hardware integration points:
- RGB/RTSP: `core/video_source.py`
- Thermal camera: `core/thermal.py`
- Sonar/range sensor: `core/sonar.py`
- LoRa/GPS SOS: `core/sos.py`

The current software prototype validates the decision pipeline. Physical sensor adapters can replace the simulation functions without changing the fusion layer.

## Configuration

Fusion weights and priority thresholds are centralized in
`config/thresholds.py` (not scattered as magic numbers across modules), so
re-tuning the decision logic is a one-file change. UI-level constants
(page title, scenario list, etc.) live in `config/settings.py`.
