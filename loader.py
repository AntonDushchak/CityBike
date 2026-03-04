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

def save_csv(path: str, df: pd.DataFrame):
    try:
        df.to_csv(path, index=False)
    except Exception as e:
        raise RuntimeError(f"Error saving {path}: {e}")