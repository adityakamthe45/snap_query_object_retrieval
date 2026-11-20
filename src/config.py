from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_config(config_path="configs/default.yaml"):
    path = Path(config_path)
    if not path.is_absolute():
        path = ROOT / path
    with open(path, "r") as f:
        return yaml.safe_load(f)
