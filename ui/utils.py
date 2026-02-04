import os
import pickle
import re
import json
from argparse import ArgumentParser
from datetime import datetime
from glob import glob
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import pandas as pd
from models import MetricQC, QCRecord

def parse_qc_config(qc_json, qc_task) -> dict:
	"""Parse a single sample QC JSON file and categorize paths.

	Returns a dict with keys:
	  - 'base_mri_image_path': Path
	  - 'overlay_mri_image_path': Path
	  - 'svg_montage_path': Path
	  - 'iqm_path': Path

	The JSON will be a dict with named paths. If the file
	doesn't exist or cannot be parsed an empty result is returned.
	All returned entries are Path objects (not resolved).
	"""

	qc_json_path = Path(qc_json) if qc_json else None
	print(f"Parsing QC config: {qc_json_path}, task: {qc_task}")

	base_mri_image_path = None
	overlay_mri_image_path = None
	svg_montage_path = None
	iqm_path = None

	try:
		if qc_json_path and qc_json_path.is_file():
			raw = json.loads(qc_json_path.read_text())			

			# check if qc_task exists in raw
			qc_task_dict = raw.get(qc_task, {})			

			if isinstance(qc_task_dict, dict):
				base_mri_image_path = Path(qc_task_dict.get("base_mri_image_path")) if qc_task_dict.get("base_mri_image_path") else None
				overlay_mri_image_path = Path(qc_task_dict.get("overlay_mri_image_path")) if qc_task_dict.get("overlay_mri_image_path") else None
				svg_montage_path = Path(qc_task_dict.get("svg_montage_path")) if qc_task_dict.get("svg_montage_path") else None
				iqm_path = Path(qc_task_dict.get("iqm_path")) if qc_task_dict.get("iqm_path") else None
	except Exception:
		pass

	return {
		"base_mri_image_path": base_mri_image_path,
		"overlay_mri_image_path": overlay_mri_image_path,
		"svg_montage_path": svg_montage_path,
		"iqm_path": iqm_path,
	}


def load_mri_data(path_dict: dict) -> dict:
	"""Load base and overlay MRI image files as bytes."""

	base_mri_path = path_dict.get("base_mri_image_path")
	overlay_mri_path = path_dict.get("overlay_mri_image_path")
	file_bytes_dict = {}

	if base_mri_path and base_mri_path.is_file():
		with open(base_mri_path, "rb") as f:
			file_bytes_dict["base_mri_image_bytes"] = f.read()
	if overlay_mri_path and overlay_mri_path.is_file():
		with open(overlay_mri_path, "rb") as f:
			file_bytes_dict["overlay_mri_image_bytes"] = f.read()

	return file_bytes_dict


def load_svg_data(path_dict: dict) -> str | None:
	"""Load SVG montage file content as string."""
	svg_montage_path = path_dict.get("svg_montage_path")
	if svg_montage_path and svg_montage_path.is_file():
		try:
			with open(svg_montage_path, "r") as f:
				return f.read()
		except Exception:
			return None
	return None


def load_iqm_data(path_dict: dict) -> dict | None:
	"""Load IQM JSON file content as dict."""
	iqm_path = path_dict.get("iqm_path")
	if iqm_path and iqm_path.is_file():
		try:
			with open(iqm_path, "r") as f:
				return json.load(f)
		except Exception:
			return None
	return None


# TODO : integrate with layout.py
def save_qc_results_to_csv(out_file, qc_records):
    """
    Save QC results from Streamlit session state to a CSV file.

    Parameters
    ----------
    out_file : str or Path
        Path where the CSV will be saved.
    qc_records : list
        List of QCRecord objects (or dicts) stored.
    """
    out_file = Path(out_file)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # Flatten metrics dynamically
    rows = []

    for rec in qc_records:
        row = {
            "subject": f"sub-{rec.subject_id}",
            "session": rec.session_id,
            "task": str(rec.task_id),
            "run": str(rec.run_id),
            "pipeline": rec.pipeline,
            "complete_timestamp": rec.complete_timestamp,
        }

        for m in rec.metrics:
            metric_name = m.name.lower().replace("-", "_")
            if m.value is not None:
                row[f"{metric_name}_value"] = m.value
            if m.qc is not None:
                row[f"{metric_name}"] = m.qc

        row.update(
            {
                "require_rerun": rec.require_rerun,
                "rater": rec.rater,
                "final_qc": rec.final_qc,
                "notes": next(
                    (m.notes for m in rec.metrics if m.name == "QC_notes"), None
                ),
            }
        )
        rows.append(row)

    df = pd.DataFrame(rows)
    if out_file.exists():
        df_existing = pd.read_csv(out_file)
        df = pd.concat([df_existing, df], ignore_index=True)
        # Drop duplicates based on all columns or a subset
        df = df.drop_duplicates(
            subset=["subject", "session", "task", "run", "pipeline"], keep="last"
        )
    df = df.sort_values(by=["subject"]).reset_index(drop=True)
    df.to_csv(out_file, index=False)

    return out_file