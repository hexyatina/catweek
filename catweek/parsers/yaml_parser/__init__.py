from pathlib import Path
from .loader import load_yaml_doc
from .normalizer import normalize_yaml_doc

def get_normalized_yaml_doc(file_path: Path) -> list[dict]:
    raw_doc = load_yaml_doc(file_path)
    return normalize_yaml_doc(raw_doc)

__all__ = ["get_normalized_yaml_doc"]