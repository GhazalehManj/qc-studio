code_dir="/home/nikhil/projects/neuroinformatics_tools/sandbox/tigrbid-QC"
pipeline_script="data/fmriprep/fmriprep_main.py"
data_dir="/home/nikhil/projects/Parkinsons/qpn/derivatives/fmriprep/23.1.3/output/"
participant_labels_tsv="/home/nikhil/projects/neuroinformatics_tools/nipoppy-sandbox/qc/qc_participants.tsv"
output_dir="/home/nikhil/projects/neuroinformatics_tools/nipoppy-sandbox/qc/output"
port_number="8501"

streamlit run $code_dir/$pipeline_script --server.port=$port_number -- \
  --fmri_dir $data_dir \
  --participant_labels $participant_labels_tsv \
  --output_dir $output_dir
