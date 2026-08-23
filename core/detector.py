from ultralytics import YOLO

from config.thresholds import YOLO_MODEL_NAME, DEFAULT_PERSON_CONFIDENCE


class PersonDetector:
    def __init__(self, model_name=YOLO_MODEL_NAME):
        self.model = YOLO(model_name)

    def detect(self, frame, conf=DEFAULT_PERSON_CONFIDENCE):
        results = self.model.predict(frame, conf=conf, classes=[0], verbose=False)
        detections = []
        for result in results:
            if result.boxes is None:
                continue
            for box in result.boxes:
                bbox = box.xyxy[0].cpu().numpy().astype(int).tolist()
                detections.append({"bbox": bbox, "confidence": float(box.conf[0])})
        detections.sort(key=lambda x: x["confidence"], reverse=True)
        return detections
