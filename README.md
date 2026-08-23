# 🚁 AERIS — Autonomous Emergency Response & Intelligence System

AERIS is an AI-assisted drone-based search-and-rescue decision-support
prototype. It turns an incoming UAV video stream into a **prioritized
rescue decision** — not just a video overlay.

```
UAV Video → AI Perception → Environmental Assessment → Thermal + Sonar + SOS
          → Sensor Fusion → Rescue Priority → Mission Recommendation
```

## Problem

During floods, disasters, and urban emergencies, rescue teams face:
- Survivors hard to identify from ground level.
- Reduced visibility from flood water and debris.
- No clear signal for *which* detected person needs help first.
- Sensor data (visual, thermal, sonar, SOS beacons) arriving independently
  instead of as one actionable decision.

AERIS converts raw UAV observations into a single ranked rescue priority
with a recommended mission action.

## What's real vs. simulated in this prototype

Be upfront about this with judges — it's the difference between a credible
prototype and an overclaim.

| Component | Status |
|---|---|
| RGB person detection | 🟢 **Real** — YOLO11n inference (`ultralytics`) on the actual video frame |
| Flood/hazard estimation | 🟢 **Real** — image-based HSV heuristic on the actual frame |
| Sensor fusion + rescue scoring | 🟢 **Real** — deterministic, unit-tested logic (`core/fusion.py`, `core/mission.py`) |
| Mission-control dashboard | 🟢 **Real** — live Streamlit app driving the full pipeline, not a mockup |
| Thermal confirmation | 🟡 **Simulated** — software interface standing in for a physical thermal camera |
| Sonar/range clearance | 🟡 **Simulated** — software interface standing in for a physical sonar/range sensor |
| SOS / LoRa beacon | 🟡 **Simulated** — demo event standing in for a physical LoRa/GPS receiver |

Simulated modules are explicitly labeled 🟡 in the UI itself, not hidden.
They're written as swappable interfaces (see **Hardware integration**
below) so real sensor adapters can replace them without touching the
fusion or mission logic.

## Core capabilities

1. **UAV video processing** — accepts a video file, USB camera, or RTSP URL.
2. **AI person detection** — YOLO-based object detection on each frame.
3. **Environmental assessment** — flood/hazard scoring from the visual scene.
4. **Multi-modal sensor fusion** — RGB + thermal + sonar + flood risk + SOS
   combined into one rescue score per target.
5. **Rescue prioritization** — every target gets `CRITICAL` / `HIGH` /
   `MEDIUM` / `LOW`.
6. **Mission recommendation** — a plain-language recommended action for the
   top-priority target.
7. **Mission visualization** — live video overlay, sensor breakdown, and an
   illustrative mission map, all in the Streamlit dashboard.

## Architecture

```
UAV / Camera
     |
     v
Video Source Layer  (core/video_source.py)
     |
     v
AI Perception  (core/detector.py — real YOLO)
     |
     +---------------+---------------+
     |               |               |
     v               v               v
  Thermal        Flood/Hazard      Sonar
 (simulated)   (real, image-based) (simulated)
     |               |               |
     +---------------+---------------+
                     |
                     v
            Sensor Fusion  (core/fusion.py)
                     |
                     v
           Rescue Priority  (core/mission.py)
                     |
                     v
          Mission Control UI  (app.py)
```

Fusion weights and priority thresholds are centralized in
`config/thresholds.py` — one file to look at (or re-tune) for "why does
this target score X%".

## Project structure

```
AERIS/
├── app.py                  # Streamlit entry point — the mission-control app
├── requirements.txt        # runtime dependencies
├── requirements-dev.txt    # + pytest, for running tests/
├── LICENSE
│
├── config/
│   ├── settings.py         # UI-level constants (title, scenarios, etc.)
│   └── thresholds.py       # fusion weights, priority bands — the "tuning knob" file
│
├── core/
│   ├── video_source.py     # video file / camera / RTSP input
│   ├── detector.py         # real YOLO person detection
│   ├── hazard.py           # real image-based flood risk
│   ├── thermal.py          # simulated thermal confirmation (swap point for hardware)
│   ├── sonar.py            # simulated sonar clearance (swap point for hardware)
│   ├── sos.py              # simulated SOS/LoRa event (swap point for hardware)
│   ├── fusion.py           # weighted sensor fusion -> rescue score + priority
│   ├── mission.py          # target ranking + recommended action
│   └── visuals.py          # video overlay + mission-map rendering
│
├── tests/                  # unit tests for the pure-logic modules (fusion, mission,
│                            # hazard, sonar) — no GPU/model download needed to run
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEMO_SCRIPT.md      # 2–3 minute demo walkthrough for round 2
│   └── JUDGE_QA.md         # anticipated judge questions and honest answers
│
├── data/README.md          # where to get a demo UAV clip
├── models/README.md        # YOLO weights auto-download on first run
└── .github/workflows/tests.yml
```

## Run it

**Recommended: run locally**, on your own laptop, for the demo. The YOLO
nano model is CPU-capable — no GPU required for a live person-detection
demo on a short clip.

```bash
git clone <your-repo-url>
cd AERIS
python3 -m venv .venv && source .venv/bin/activate      # optional but recommended
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).
The first run downloads `yolo11n.pt` automatically — do this once **before**
you're in front of judges if you're not sure about venue Wi-Fi.

In the sidebar: upload a short UAV/aerial clip with visible people (see
`data/README.md` for where to get one), or switch to Camera/RTSP mode and
use `0` for a laptop webcam. Press **START MISSION**.

### Why not Streamlit Community Cloud for the live demo?

You *can* deploy there for a shareable link, but for the actual judging
demo, local is safer: webcam/RTSP access doesn't work from a cloud-hosted
app, and free-tier cloud CPU/memory limits can make YOLO inference
noticeably slower than your own laptop. Use cloud deployment as a backup
"here's the link" artifact, not as your primary demo path.

### Running tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

Tests cover the fusion scoring, mission ranking, and the flood/sonar
heuristics — the parts of the pipeline that are deterministic and don't
need a model download to verify. CI runs these on every push
(`.github/workflows/tests.yml`).

## Hardware integration (next deployment layer)

Every simulated module is a small, isolated function with one clear job —
swap the function body, keep the signature, and the fusion/mission layers
need no changes:

| Interface | File | Replace with |
|---|---|---|
| RGB/RTSP | `core/video_source.py` | already accepts a real RTSP URL |
| Thermal camera | `core/thermal.py` | real thermal-frame processing |
| Sonar/range sensor | `core/sonar.py` | real sonar/range driver |
| LoRa/GPS SOS | `core/sos.py` | real LoRa/GPS receiver integration |

## Demo script

See `docs/DEMO_SCRIPT.md` for a tight 2–3 minute walkthrough, and
`docs/JUDGE_QA.md` for how to answer the "is this real?" questions
honestly and confidently.

## Vision

AERIS aims to give rescue teams an intelligent aerial decision-support
system that turns raw disaster-scene observations into actionable rescue
priorities — starting from a real, working perception-and-fusion pipeline,
with hardware sensor integration as the next layer, not a redesign.
