"""General utilities for the backend"""
# External libraries
import pandas as pd

def load_dataframe(kind: str = "csv", connection_path: (str | None) = None):
    if isinstance(connection_path, type(None)):
        raise ValueError("Invalid connection_path (None).")
    if kind == "csv":
        return pd.read_csv(connection_path, sep=";")
    elif kind == "excel":
        return pd.read_excel(connection_path)
    else:
        raise ValueError(f"Invalid kind ({kind}).")

def get_prerequisites(prerequisites):
    if prerequisites == [""]:
        return []
    return [
        i[:i.index(" (")].strip()
        for i in prerequisites
    ]

def get_blocks():
    return []
