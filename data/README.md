# Demo footage

This folder is intentionally not pre-populated with video (`.gitignore` also
excludes `*.mp4/.avi/.mov/.mkv` so large binaries don't bloat the repo).

You need a short (30–90s) clip with **real, visible people** in frame —
YOLO detects real human shapes, so synthetic/animated footage will not
produce detections.

Good sources for a demo clip, in order of ease:

1. **Record it yourself.** A phone clip from a balcony/rooftop looking down
   at 1–3 people standing/sitting on the ground works well and is the most
   controllable option for a live demo.
2. **Free stock footage** — search terms like "aerial flood rescue",
   "drone search and rescue", "UAV disaster footage" on Pexels or Pixabay
   (both offer royalty-free video with no attribution required).
3. **Public disaster-response B-roll** from news agencies, used only for
   an internal hackathon demo, not redistribution.

Drop the file anywhere convenient and upload it through the Streamlit
sidebar ("Upload UAV footage") — it doesn't need to live in this folder.

## Camera / RTSP alternative

For the live-camera demo mode, a laptop webcam pointed at a person standing
in for a "survivor" works as well as recorded footage — set the source to
`0` (or your webcam index) instead of uploading a file.
