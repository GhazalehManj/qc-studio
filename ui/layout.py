import os
from pathlib import Path
import streamlit as st
from niivue_component import niivue_viewer
from utils import parse_qc_config, load_mri_data, load_svg_data

def niivue_viewer_from_path(filepath: str, height: int = 600, key: str | None = None) -> None:
	"""Helper to read a local NIfTI file and call the niivue component (if available).

	This mirrors the project's existing helper behavior: read the file bytes and
	hand them to the component. If the niivue component is not installed/available,
	a friendly warning is shown instead.
	"""
	if niivue_viewer is None:
		st.warning(
			"NiiVue component not available. Install the project's `niivue_component` or run the example in `ui/niivue_test.py` to preview behavior."
		)
		return

	if not os.path.isfile(filepath):
		st.error(f"NIfTI file not found: {filepath}")
		return

	with open(filepath, "rb") as f:
		file_bytes = f.read()

	if key is None:
		key = f"niivue_viewer_{os.path.basename(filepath)}"

	# call the underlying component
	try:
		niivue_viewer(nifti_data=file_bytes, filename=os.path.basename(filepath), height=height, key=key)
	except Exception as e:
		st.error(f"Failed to render niivue viewer: {e}")


def app(participant_id, session_id, qc_pipeline, qc_task, qc_config_path: str | None = None) -> None:
	"""Main Streamlit layout: top inputs, middle two viewers, bottom QC controls."""
	st.set_page_config(layout="wide")

	# Top container: inputs
	top = st.container()
	with top:
		st.title("Welcome to Nipoppy QC-Studio! 🚀")
		# qc_pipeline = "fMRIPrep"
		# qc_task = "sdc-wf"
		st.subheader(f"QC Pipeline: {qc_pipeline}, QC task: {qc_task}")

		# show participant and session
		st.write(f"Participant ID: {participant_id} | Session ID: {session_id}")		

		# Rater info
		rater_name = st.text_input("Rater name:")
		st.write("You entered:", rater_name)

		# Input rater experience as choice box
		options = ["Beginner (< 1 year experience)", "Intermediate (1-5 year experience)", "Expert (>5 year experience)"]
		experience_level = st.selectbox("Rater experience level:", options)
		st.write("Experience level:", experience_level)

	# parse qc config
	qc_config = parse_qc_config(qc_config_path, qc_task) 
	print(f"qc config: {qc_config_path}, {qc_config}")

	# Middle: two side-by-side viewers
	middle = st.container()
	with middle:
		niivue_col, svg_col = st.columns([0.4, 0.6], gap="small")

		with niivue_col:
			st.header("3D MRI (Niivue)")
			# Show mri
			mri_data = load_mri_data(qc_config)
			if "base_mri_image_bytes" in mri_data:
				try:
					niivue_viewer(
						nifti_data=mri_data["base_mri_image_bytes"],
						filename=str(qc_config.get("base_mri_image_path").name) if qc_config.get("base_mri_image_path") else "base_mri.nii",
						height=600,
						key="niivue_base_mri",
					)
				except Exception as e:
					st.error(f"Failed to load base MRI in Niivue viewer: {e}")
			else:
				st.info("Base MRI image not found or could not be loaded.")

			# TODO : Optionally overlay another image

		with svg_col:
			st.header("SVG Montage")
			# Show SVG montage
			svg_data = load_svg_data(qc_config)
			if svg_data:
				st.components.v1.html(svg_data, height=600, scrolling=True)
			else:
				st.info("SVG montage not found or could not be loaded.")

	# Bottom: QC metrics and radio buttons
	bottom = st.container()
	with bottom:
		# st.header("QC: Rating & Metrics")
		rating_col, iqm_col = st.columns([0.4, 0.6], gap="small")
		with iqm_col:
			st.subheader("QC Metrics")
			# Placeholder: user may compute or display metrics here
			st.write("Add QC metrics here (e.g., SNR, motion). This is a placeholder area.")

		with rating_col:
			st.subheader("Quality Scores")
			rating = st.radio("Rate this subject:", options=("PASS", "FAIL", "UNCERTAIN"), index=0)
			notes = st.text_area("Notes (optional):")
			if st.button("💾 Save QC results to CSV", width=1000):
				# save for the current participant
				st.success(f"Saved rating for {participant_id}: {rating}")
				# For now, just print — wiring to persistent storage can be added later
				st.write({"subject": participant_id, "rating": rating, "notes": notes})

                # TODO				
                # out_path = save_qc_results_to_csv(out_file, qc_records)
                # st.success(f"QC results saved to: {out_path}")


if __name__ == "__main__":
	# Example invocation for local testing; replace with real values when integrating.
	# get current directory
	
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")
	
    qc_config_path = os.path.join(current_dir, "sample_qc.json")
    qc_workflow = "anat_wf_qc"
    pipeline = "fMRIPrep"
    participant_id = "sub-01"
    session_id = "ses-01"
	
    app(
        participant_id=participant_id,
        session_id=session_id,
        qc_pipeline=pipeline,
        qc_task=qc_workflow,
        qc_config_path=qc_config_path,
    )
	
