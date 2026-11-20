
# Run this locally from the repo root . Creates metadata.json for the Streamlit app.

import json
from src.inference import YOLOv11Inference

metadata = YOLOv11Inference("yolo11m.pt").process_directory("data_for_prj")
with open("metadata.json", "w") as f:
    json.dump(metadata, f)
print(f"Saved metadata.json for {len(metadata)} images")
