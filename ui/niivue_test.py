import streamlit as st
from niivue_component import niivue_viewer

uploaded_file = st.file_uploader("Choose a NIFTI file", type=["nii", "nii.gz", "tck.gz"])

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    niivue_viewer(
        nifti_data=file_bytes,
        filename=uploaded_file.name,
        height=600,
        key="niivue_viewer"
    )