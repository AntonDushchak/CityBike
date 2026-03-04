from pathlib import Path
from typing import Union

import pandas as pd


def load_csv(path) -> pd.DataFrame:
    import os

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Error loading {path}: {e}")
    return df


def _ensure_parent(path: Union[str, Path]) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def save_csv(path: str, df: pd.DataFrame):
    target = _ensure_parent(path)
    try:
        df.to_csv(target, index=False)
    except Exception as e:
        raise RuntimeError(f"Error saving {target}: {e}")


def save_txt(path: str, contents: str, encoding: str = "utf-8"):
    target = _ensure_parent(path)
    try:
        target.write_text(contents, encoding=encoding)
    except Exception as e:
        raise RuntimeError(f"Error saving text {target}: {e}")