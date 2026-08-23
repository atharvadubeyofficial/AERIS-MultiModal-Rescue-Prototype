# Models

`core/detector.py` loads `yolo11n.pt` (the Ultralytics YOLO11-nano weights)
by name. `ultralytics` downloads it automatically into this folder on first
run — there's nothing to manually place here before running the app.

If your demo machine has no internet access at judging time, run the app
once beforehand (with internet) so the weights are cached locally, or
pre-download and commit-ignore the `.pt` file (it's already covered by
standard `.gitignore` patterns for large binaries — add `models/*.pt`
explicitly if you want to be sure it never gets committed).
