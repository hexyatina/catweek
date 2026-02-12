from pathlib import Path
from .loader import load_yaml_doc
from .normalizer import normalize_yaml_doc

def get_normalized_yaml_doc(file_path: Path, verbose: bool = False) -> list[dict]:
    if verbose:
        print(f" [Parser] Reading {file_path.name}...")
    raw_doc = load_yaml_doc(file_path)
    normalized = normalize_yaml_doc(raw_doc)
    if verbose:
        print(f" [Parser] Normalized {len(normalized)} rows.")
    return normalized

__all__ = ["get_normalized_yaml_doc"]