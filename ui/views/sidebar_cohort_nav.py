"""Multipage sidebar: one control per subject with QC-done marker (Streamlit app sidebar)."""

import streamlit as st

from constants import MESSAGES
from managers.session_manager import SessionManager


def render_sidebar_cohort_subjects(
	*,
	participant_ids: list,
	total_participants: int,
	qc_task: str,
	session_id: str = "ses-01",
	entrypoint_rel_path: str | None = None,
) -> None:
	"""Add a **Subjects** block under the built-in page list: ✅ if QC saved, ⬜ otherwise.

	Each row is a full-width button that jumps to that participant (same as main pagination).
	When ``entrypoint_rel_path`` is set (e.g. ``\"main.py\"``), uses ``st.switch_page`` so
	multipage flows return to the QC entrypoint.
	"""
	if not SessionManager.is_landing_page_complete():
		return
	ids = list(participant_ids or [])[: max(int(total_participants), 0)]
	if not ids:
		return

	st.sidebar.divider()
	st.sidebar.caption(MESSAGES["sidebar_subjects_header"])
	current_page = SessionManager.get_current_page()
	for i, pid_raw in enumerate(ids):
		page_num = i + 1
		pid = str(pid_raw)
		done = SessionManager.participant_has_decided_qc(pid, session_id, qc_task)
		mark = "✅" if done else "⬜"
		display_pid = pid if len(pid) <= 36 else f"{pid[:33]}..."
		suffix = " — current" if page_num == current_page else ""
		label = f"{mark} {display_pid}{suffix}"
		if st.sidebar.button(label, key=f"sidebar_cohort_nav_{i}", width="stretch"):
			SessionManager.set_current_page(page_num)
			if entrypoint_rel_path:
				st.switch_page(entrypoint_rel_path)
			else:
				st.rerun()
