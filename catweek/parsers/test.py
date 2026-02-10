from pathlib import Path
import yaml
from pprint import pprint

from catweek.parsers.yaml_parser.loader import load_yaml
from catweek.parsers.yaml_parser.normalize import normalize_yaml

BASE_DIR = Path(__file__).resolve().parents[2]

YAML_DIR = (
    BASE_DIR
    / "catweek"
    / "data"
    / "schedules"
    / "IPZ"
    / "IPZ-3"
)
YAML_FILES = {
    (YAML_DIR / "IPZ-31.yaml"),
    (YAML_DIR / "IPZ-32.yaml"),
    (YAML_DIR / "IPZ-33.yaml"),
}
def main(yaml_file):
    print("=== Loading YAML ===")
    schedules = load_yaml(yaml_file)

    print(f"\nLoaded {len(schedules)} schedule document(s)\n")

    print("=== Parsed & Validated (Pydantic) ===")
    for s in schedules:
        pprint(s.model_dump())
        print("-" * 60)

    print("\n=== Normalized ===")
    normalized = normalize_yaml(schedules)

    print(f"Total lessons: {len(normalized)}\n")
    pprint(normalized)


if __name__ == "__main__":
    main((YAML_DIR / "IPZ-32.yaml"))