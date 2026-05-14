#!/usr/bin/env bash
# Run QC-Studio against bundled fMRIPrep sample data (invoke from this directory: cd ui && ./fmriprep_test.sh)
#
# Optional first argument: path to qc.json (relative to this directory or absolute).
# Examples:
#   ./fmriprep_test.sh
#   ./fmriprep_test.sh ../pipelines/demo/qc_fmriprep_montage_alt.json
#   QC_JSON=../pipelines/demo/qc.json ./fmriprep_test.sh   # same as default

set -euo pipefail

qc_launch_script="main.py"
qc_pipeline="fmriprep"
qc_task="anat_wf_qc"
qc_json="${1:-${QC_JSON:-../pipelines/demo/qc.json}}"
dataset_dir="../sample_data"
participant_list="../sample_data/qc_participants.tsv"
output_dir="./output"
port_number="${PORT:-8501}"

echo "Using qc_json=${qc_json}  port=${port_number}"

streamlit run "$qc_launch_script" --server.port="$port_number" -- \
  --qc_json "$qc_json" \
  --qc_task "$qc_task" \
  --qc_pipeline "$qc_pipeline" \
  --dataset_dir "$dataset_dir" \
  --participant_list "$participant_list" \
  --output_dir "$output_dir"
