from pathlib import Path

import torch
from ultralytics import YOLO

from src.config import load_config


def _relative_posix(path) -> str:
   
    path = Path(path)
    try:
        path = path.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        pass
    return path.as_posix()


class YOLOv11Inference:

    def __init__(self, model_name):
        self.model = YOLO(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        config = load_config()
        self.conf_threshold = config["model"]["conf_threshold"]
        self.image_extensions = {e.lower() for e in config["data"]["image_extensions"]}

    def process_image(self, image_path):
        results = self.model.predict(source=str(image_path),
                                     conf=self.conf_threshold,
                                     device=self.device,
                                     verbose=False)
        detection = []
        class_counts = {}
        for result in results:  
            for box in result.boxes:
                cls = result.names[int(box.cls)]
                detection.append({
                    "class": cls,
                    "confidence": float(box.conf),
                    "bbox": box.xyxy[0].tolist(),
                    "count": 1,
                })
                class_counts[cls] = class_counts.get(cls, 0) + 1

        for det in detection:
            det["count"] = class_counts[det["class"]]

        return {
            "image_path": _relative_posix(image_path),
            "detections": detection,
            "total_objects": len(detection),
            "unique_class": list(class_counts.keys()),
            "class_counts": class_counts,
        }

    def process_directory(self, image_dir):
        
        image_paths = sorted(
            p for p in Path(image_dir).iterdir()
            if p.is_file() and p.suffix.lower() in self.image_extensions
        )
        metadata = []
        for img_path in image_paths:
            try:
                metadata.append(self.process_image(img_path))
            except Exception as e:
                print(f"Error processing the image {img_path}: {e}")
        return metadata
