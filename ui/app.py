import streamlit as st
from utils.config import parse_qc_config
from managers.session_manager import SessionManager
from views.landing_page import show_landing_page
from views.congratulations_page import show_congratulations_page
from components.qc_viewer import display_qc_viewers


def app(dataset_dir, participant_id, session_id, qc_pipeline, qc_task, qc_config_path, out_dir, total_participants, drop_duplicates, participant_list, participant_ids=None) -> None:
	"""Main Streamlit layout: landing page, QC viewers, and congratulations."""
	st.set_page_config(layout="wide")

	# Initialize session state
	SessionManager.init_session_state()
	SessionManager.compact_duplicate_qc_records_if_needed()

	# Check if we're on the landing page
	if not SessionManager.is_landing_page_complete():
		show_landing_page(qc_pipeline, qc_task, out_dir, participant_list, qc_config_path)
		return

	# Check if we're on the final congratulations page (past last index)
	if participant_id is None:
		cohort_complete = (not participant_ids) or SessionManager.all_cohort_qc_complete(
			qc_task, session_id, participant_ids
		)
		show_congratulations_page(
			qc_task,
			out_dir,
			total_participants,
			drop_duplicates,
			cohort_complete=cohort_complete,
			participant_ids=participant_ids,
			session_id=session_id,
		)
		return

	# parse qc config
	substitution_values = {
		'participant_id': participant_id,
		'session_id': session_id
	}
	qc_config = parse_qc_config(qc_config_path, qc_task, substitution_values)

	# Display QC Viewers with integrated pagination in left sidebar
	display_qc_viewers(
		dataset_dir=dataset_dir,
		qc_config=qc_config,
		participant_id=participant_id,
		session_id=session_id,
		qc_pipeline=qc_pipeline,
		qc_task=qc_task,
		total_participants=total_participants,
		participant_ids=participant_ids,
	)
