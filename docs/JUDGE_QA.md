# Anticipated Judge Q&A

Be direct and honest about what's real vs. simulated in the prototype — judges
respect that far more than an overclaim that falls apart under a follow-up
question.

**Q: Is the thermal/sonar data real?**
No. RGB detection and the flood-risk heuristic run on real image data. Thermal
and sonar are simulated software interfaces (`core/thermal.py`,
`core/sonar.py`) so the fusion and mission logic can be built and demoed
before physical sensors are integrated. This is stated on-screen in the UI
(🟡 SIMULATED) and in the README, not hidden.

**Q: Why simulate instead of using real thermal/sonar hardware?**
Time and hardware access in a hackathon. The architecture is deliberately
modular: `core/fusion.py` and `core/mission.py` only consume a confidence
value in [0, 1] — they don't care whether it came from a simulator or a real
sensor adapter. Swapping `simulation/thermal_simulator.py`-style logic for
`hardware/thermal_camera.py` requires no change to the fusion or mission
layers. That's the actual point of the fusion architecture: sensors are
pluggable interfaces.

**Q: What's actually real in this prototype?**
- Person detection: real YOLO (`ultralytics`) inference on the video frame.
- Flood/hazard estimation: a real image heuristic (HSV water-color ratio),
  not a hardcoded number.
- Fusion scoring and priority ranking: real, deterministic, testable logic
  (`core/fusion.py`, `core/mission.py`) — see `tests/`.
- Mission-control UI: a real Streamlit app driving the whole pipeline live,
  not a static mockup.

**Q: How would this scale to a real deployment?**
Three layers would need hardening before field use: (1) real thermal/sonar/
LoRa hardware adapters behind the existing interfaces, (2) a proper video
ingest layer for a live drone RTSP feed with reconnection handling, and
(3) moving fusion weights (`config/thresholds.py`) from fixed constants to
values tuned against labeled disaster-response data.

**Q: Why these specific fusion weights?**
They're a starting, explainable prior — RGB detection confidence weighted
highest (0.30) since it's the only always-real signal, thermal next (0.25)
as the strongest independent confirmation once hardware exists, flood risk
(0.20) because it changes urgency, sonar (0.15) for approach safety, and SOS
(0.10) as a rare but very strong positive signal. They live in one file
(`config/thresholds.py`) specifically so they can be re-tuned without
touching pipeline code.

**Q: What happens if the drone loses the video feed mid-mission?**
The video source read fails gracefully — the app reports "Mission stream
ended" and stops the loop instead of crashing. A per-frame try/except also
guards the detector so one bad frame doesn't kill a live demo.

**Q: Can this run on a real drone's onboard compute?**
The nano YOLO model (`yolo11n.pt`) is CPU-capable, so the perception layer
can run on modest hardware; for airborne edge deployment you'd want an
edge accelerator (e.g. Jetson-class board) rather than relying on a ground
laptop, but that's a deployment decision, not a code change.
