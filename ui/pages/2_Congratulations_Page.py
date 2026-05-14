"""Multipage sidebar entry: QC complete / congratulations summary.

The full UI lives in ``views/congratulations_page.py``; this file only wires CLI
context so Streamlit can run the page when selected from the left navigation.
"""
import streamlit as st

from main import get_cli_run_context
from managers.session_manager import SessionManager
from views.congratulations_page import show_congratulations_page
from views.sidebar_cohort_nav import render_sidebar_cohort_subjects

st.set_page_config(layout="wide")
ctx = get_cli_run_context()
SessionManager.init_session_state()
SessionManager.compact_duplicate_qc_records_if_needed()
render_sidebar_cohort_subjects(
	participant_ids=ctx.get("participant_ids") or [],
	total_participants=ctx["total_participants"],
	qc_task=ctx["qc_task"],
	session_id="ses-01",
	entrypoint_rel_path="main.py",
)
session_id = "ses-01"
pids = ctx.get("participant_ids") or []
cohort_complete = (not pids) or SessionManager.all_cohort_qc_complete(
	ctx["qc_task"], session_id, pids
)
show_congratulations_page(
	ctx["qc_task"],
	ctx["out_dir"],
	ctx["total_participants"],
	ctx["drop_duplicates"],
	cohort_complete=cohort_complete,
	participant_ids=pids or None,
	session_id=session_id,
	entrypoint_rel_path="main.py",
)
