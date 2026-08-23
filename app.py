import time
import tempfile
from pathlib import Path
import cv2
import streamlit as st

from core.video_source import VideoSource
from core.detector import PersonDetector
from core.hazard import estimate_flood_risk
from core.thermal import estimate_thermal_confirmation
from core.sonar import estimate_sonar_clearance
from core.sos import get_sos_state
from core.fusion import fuse_target
from core.mission import rank_targets, mission_action
from core.visuals import draw_detections, mission_map_image
from config.settings import (
    APP_TITLE, APP_ICON, APP_CAPTION, SCENARIOS, VIDEO_FILE_TYPES,
    FRAME_DELAY_SECONDS, SENSOR_STATUS_LABELS,
)
from config.thresholds import DEFAULT_PERSON_CONFIDENCE, DEFAULT_MAX_TARGETS

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
st.title(f"{APP_ICON} {APP_TITLE}")
st.caption(APP_CAPTION)

with st.sidebar:
    st.header("Mission Setup")
    scenario = st.selectbox("Scenario", SCENARIOS)
    source_mode = st.radio("Video Source", ["Demo / Uploaded Video", "Camera / RTSP"])
    source_value = None

    if source_mode == "Demo / Uploaded Video":
        uploaded = st.file_uploader("Upload UAV footage", type=VIDEO_FILE_TYPES)
        if uploaded:
            suffix = Path(uploaded.name).suffix or ".mp4"
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(uploaded.read())
            tmp.close()
            source_value = tmp.name
    else:
        source_value = st.text_input("Camera index or RTSP URL", "0")

    conf = st.slider("Person confidence", 0.20, 0.80, DEFAULT_PERSON_CONFIDENCE, 0.05)
    max_targets = st.slider("Max targets", 1, 10, DEFAULT_MAX_TARGETS)
    st.divider()
    for dot, label, status in SENSOR_STATUS_LABELS:
        st.write(f"{dot} {label}: {status}")
    start = st.button("🚨 START MISSION", type="primary", use_container_width=True)
    stop = st.button("⏹ STOP", use_container_width=True)

if "running" not in st.session_state:
    st.session_state.running = False
if start:
    st.session_state.running = True
if stop:
    st.session_state.running = False

if not st.session_state.running:
    st.info("Configure the mission and press START MISSION.")
    st.markdown("**UAV stream → AI perception → hazard assessment → sensor fusion → rescue priority → mission action**")
    st.stop()

if source_value is None:
    st.warning("Upload a short UAV video or provide a camera/RTSP source first.")
    st.stop()

@st.cache_resource
def load_detector():
    return PersonDetector()

detector = load_detector()
source = VideoSource(source_value)

frame_slot = st.empty()
metric_slot = st.empty()
target_slot = st.empty()
map_slot = st.empty()
status_slot = st.empty()

frame_count = 0

while st.session_state.running:
    ok, frame = source.read()
    if not ok:
        status_slot.warning("Mission stream ended.")
        break

    frame_count += 1
    try:
        detections = detector.detect(frame, conf=conf)
    except Exception as exc:  # keep the mission loop alive during a live demo
        status_slot.error(f"Detector error on frame {frame_count}: {exc}")
        detections = []
    flood_risk = estimate_flood_risk(frame)
    sos = get_sos_state(frame_count)

    targets = []
    for idx, det in enumerate(detections[:max_targets], start=1):
        thermal = estimate_thermal_confirmation(frame, det["bbox"], det["confidence"])
        sonar = estimate_sonar_clearance(frame, det["bbox"])
        result = fuse_target(
            idx, det["confidence"], thermal, flood_risk, sonar, sos
        )
        result["bbox"] = det["bbox"]
        targets.append(result)

    ranked = rank_targets(targets)
    annotated = draw_detections(frame.copy(), ranked)

    frame_slot.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
                     channels="RGB", use_container_width=True)

    critical = ranked[0] if ranked else None
    with metric_slot.container():
        a,b,c,d = st.columns(4)
        a.metric("Persons Detected", len(detections))
        b.metric("Flood/Hazard Risk", f"{flood_risk:.0%}")
        c.metric("SOS", "ACTIVE" if sos else "Monitoring")
        d.metric("Top Rescue Score", f"{critical['score']:.1f}%" if critical else "—")

    if critical:
        with target_slot.container():
            st.subheader(f"🎯 TARGET #{critical['target_id']} — {critical['priority']}")
            a,b,c,d,e = st.columns(5)
            a.metric("RGB", f"{critical['person_confidence']:.0%}")
            b.metric("Thermal*", f"{critical['thermal_confidence']:.0%}")
            c.metric("Flood", f"{critical['flood_risk']:.0%}")
            d.metric("Sonar*", f"{critical['sonar_clearance']:.0%}")
            e.metric("Fusion", f"{critical['score']:.1f}%")
            st.success(mission_action(critical))

    map_slot.image(mission_map_image(frame.shape[1], frame.shape[0], ranked),
                   channels="RGB", use_container_width=True)
    status_slot.caption(f"Frame {frame_count} | *Thermal and sonar are prototype simulations.")
    time.sleep(FRAME_DELAY_SECONDS)

source.release()
st.session_state.running = False
