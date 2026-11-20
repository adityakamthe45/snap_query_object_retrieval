import json
from pathlib import Path


def ensure_path_exists(raw_path):
    raw_path = Path(raw_path)
    processed_path = raw_path.parent.parent / "processed" / raw_path.name
    processed_path.mkdir(parents=True, exist_ok=True)
    return processed_path


def save_metadata(metadata, raw_path):
    processed_path = ensure_path_exists(raw_path)
    output_path = processed_path / "metadata.json"
    with open(output_path, "w") as f:   
        json.dump(metadata, f)
    return output_path


def load_metadata(metadata_path):
    metadata_path = Path(metadata_path)
    if not metadata_path.exists():
        processed_path = metadata_path.parent.parent / "processed" / metadata_path.name / "metadata.json"
        if processed_path.exists():
            metadata_path = processed_path
        else:
            raise FileNotFoundError(f"Metadata not found at {metadata_path}")
    elif metadata_path.is_dir():
        metadata_path = metadata_path / "metadata.json"

    with open(metadata_path, "r") as f:
        return json.load(f)


def get_unique_classes_counts(metadata):
    unique_classes = set()
    count_options = {}

    for item in metadata:
        for det in item["detections"]:
            unique_classes.add(det["class"])
            count_options.setdefault(det["class"], set()).add(det["count"])

    unique_classes = sorted(unique_classes)
    for cls in count_options:
        count_options[cls] = sorted(count_options[cls])

    return unique_classes, count_options
