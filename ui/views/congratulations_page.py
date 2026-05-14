"""Congratulations page component for QC-Studio UI."""
from pathlib import Path
import streamlit as st
from constants import MESSAGES, SUCCESS_MESSAGES, INFO_MESSAGES, SESSION_KEYS, QC_RATINGS
from managers.session_manager import SessionManager
from utils.export import save_qc_results_to_csv


def show_congratulations_page(
	qc_task: str,
	out_dir: str,
	total_participants: int,
	drop_duplicates: bool,
	*,
	cohort_complete: bool = True,
	participant_ids: list | None = None,
	session_id: str | None = None,
	entrypoint_rel_path: str | None = None,
) -> None:
	"""Display congratulations (full summary) or a minimal placeholder until all subjects are QC'd.

	Args:
		qc_task: QC task name
		out_dir: Output directory path
		total_participants: Total number of participants in the QC session
		drop_duplicates: Whether to drop duplicate records before saving
		cohort_complete: When False, show a minimal page (not all subjects have a decided rating).
		participant_ids: Cohort order (for Continue QC navigation).
		session_id: BIDS session id (e.g. ses-01) for completion checks.
		entrypoint_rel_path: If set (e.g. ``"main.py"``), sidebar navigation uses ``st.switch_page``.
	"""
	if not cohort_complete:
		st.subheader("QC not finished yet")
		st.info(
			"Not every participant has a PASS / FAIL / UNCERTAIN rating yet. "
			"When you are ready, use **Continue QC** to return to the review."
		)
		if participant_ids and session_id and st.button("Continue QC", key="congrats_continue_qc_incomplete"):
			miss = SessionManager.first_page_missing_qc(qc_task, session_id, participant_ids)
			st.session_state[SESSION_KEYS["current_page"]] = miss
			if entrypoint_rel_path:
				st.switch_page(entrypoint_rel_path)
			st.rerun()
		return

	st.title(MESSAGES["congratulations_title"])

	record_list = SessionManager.get_latest_qc_records_per_dedup(qc_task)
	num_reviewed = len([r for r in record_list if SessionManager._final_qc_is_decided(r)])

	st.markdown(f"""
	## {num_reviewed} participant(s) have been reviewed!

	Thank you for completing the quality control process. Your thorough review ensures the integrity of our data!

	✅ All QC records have been automatically saved.

	""")

	rater_id = SessionManager.get_rater_id()
	# Display session information and results summary
	_display_session_summary(rater_id, qc_task, record_list, reviewed_count=num_reviewed)

	# Action buttons
	col1, col2, col3 = st.columns([1, 1, 1])
	with col1:
		if st.button(MESSAGES["export_results_button"], width="stretch"):
			export_rows = SessionManager.get_latest_qc_records_per_dedup(None)
			_export_qc_results(rater_id, out_dir, export_rows, drop_duplicates)
	with col2:
		if st.button(MESSAGES["previous_button"], width="stretch"):
			SessionManager.previous_page()
			if entrypoint_rel_path:
				st.switch_page(entrypoint_rel_path)
			st.rerun()
	with col3:
		if st.button(MESSAGES["start_over_button"], width="stretch"):
			SessionManager.set_landing_page_complete(False)
			if entrypoint_rel_path:
				st.switch_page(entrypoint_rel_path)
			st.rerun()


def _display_session_summary(
	rater_id: str, qc_task: str, record_list: list, *, reviewed_count: int | None = None
) -> None:
	"""Display summary of the QC session.

	Args:
		rater_id: Rater ID
		qc_task: QC task name
		record_list: QC records for this task (deduplicated)
		reviewed_count: Participants with a decided rating; defaults to len(record_list)
	"""
	col1, col2 = st.columns([1, 1])
	with col1:
		st.subheader("Session Information")
		st.write(f"**Rater ID:** {rater_id}")
		st.write(f"**QC Task:** {qc_task}")
		n_rev = reviewed_count if reviewed_count is not None else len(record_list)
		st.write(f"**Total Participants Reviewed:** {n_rev}")

	with col2:
		st.subheader("QC Results Summary")
		# Count final_qc values
		if record_list:
			final_qc_counts = {}
			for record in record_list:
				qc_value = record.final_qc
				if qc_value not in QC_RATINGS:
					final_qc_counts["Unrated"] = final_qc_counts.get("Unrated", 0) + 1
				else:
					final_qc_counts[qc_value] = final_qc_counts.get(qc_value, 0) + 1

			for qc_status, count in sorted(final_qc_counts.items()):
				st.write(f"**{qc_status}:** {count}")


def _export_qc_results(rater_id: str, out_dir: str, record_list: list, drop_duplicates: bool) -> None:
	"""Export QC results to file.

	Args:
		rater_id: Rater ID
		out_dir: Output directory path
		record_list: List of QC records to export
		drop_duplicates: Whether to drop duplicate records
	"""
	out_file = Path(out_dir) / f"{rater_id}_QC_status.tsv"
	if record_list:
		out_path = save_qc_results_to_csv(out_file, record_list, drop_duplicates)
		st.success(SUCCESS_MESSAGES["records_exported"].format(path=out_path))
	else:
		st.info(INFO_MESSAGES["no_export_records"])
