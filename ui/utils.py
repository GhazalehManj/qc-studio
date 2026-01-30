import os
import pickle
import re
import json
from argparse import ArgumentParser
from datetime import datetime
from glob import glob
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from functools import wraps

def load_json(qc_files_json: str) -> Optional[List[Path]]:
    """
    Load a JSON file containing a list of SVG file paths.
    Validates that the top-level structure is a list.
    Returns a list of Path objects or None if no file provided.
    """
    qc_files_json = Path(qc_files_json)
    if not qc_files_json.exists():
        raise FileNotFoundError(f"JSON not found: {qc_files_json}")
    try:
        with open(qc_files_json, "r") as fh:
            raw = json.load(fh)
    except Exception as e:
        raise RuntimeError(f"Failed to parse JSON file {qc_files_json}: {e}")

    if not isinstance(raw, list):
        raise ValueError("JSON must contain a top-level list of file paths")
    
    loaded_file_list = [Path(p) for p in raw]

    return loaded_file_list