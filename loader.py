"""CSV and text file I/O utilities."""

import os
from pathlib import Path
from typing import Union

import pandas as pd


def load_csv(path: Union[str, Path]) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame.

    Args:
        path: Filesystem path to the CSV file.

    Returns:
        DataFrame containing the CSV data.

    Raises:
        FileNotFoundError: If the file does not exist.
        RuntimeError: If reading fails for any other reason.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Error loading {path}: {e}") from e
    return df


def _ensure_parent(path: Union[str, Path]) -> Path:
    """Create parent directories if they do not exist and return Path object."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def save_csv(path: Union[str, Path], df: pd.DataFrame) -> None:
    """Save a DataFrame to a CSV file.

    Args:
        path: Destination file path.
        df: DataFrame to save.

    Raises:
        RuntimeError: If writing fails.
    """
    target = _ensure_parent(path)
    try:
        df.to_csv(target, index=False)
    except Exception as e:
        raise RuntimeError(f"Error saving {target}: {e}") from e


def save_txt(path: Union[str, Path], contents: str, encoding: str = "utf-8") -> None:
    """Save text content to a file.

    Args:
        path: Destination file path.
        contents: Text to write.
        encoding: File encoding (default UTF-8).

    Raises:
        RuntimeError: If writing fails.
    """
    target = _ensure_parent(path)
    try:
        target.write_text(contents, encoding=encoding)
    except Exception as e:
        raise RuntimeError(f"Error saving text {target}: {e}") from e