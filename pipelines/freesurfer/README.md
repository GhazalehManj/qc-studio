# FreeSurfer QC configuration

QC-Studio loads **only** `qc.json` from this folder. Run `streamlit run ui/main.py …` from the repository root, or use **`ui/freesurfer_test.sh`** (from `ui/`) for the same defaults.

Example (after `cd` to the qc-studio root):

```bash
streamlit run ui/main.py --server.port=8501 -- \
  --qc_json ../pipelines/freesurfer/qc.json \
  --qc_task anat_wf_qc \
  --qc_pipeline freesurfer \
  --dataset_dir sample_data/fmriprep \
  --participant_list sample_data/qc_participants.tsv \
  --session_list ses-01,ses-02 \
  --output_dir ./output
```

Use **`--session_list`** with comma-separated BIDS session labels (e.g. `ses-01,ses-02`). The app builds one review **page** per **(participant × session)** from your participant list. If `qc_participants.tsv` includes a **`session_id`** column, that file defines the exact rows instead (one row per participant–session pair).

### Multiple tasks in `qc.json`

This bundle defines a **single** task (`anat_wf_qc`). **`--qc_task all`** is equivalent to that one task. To run from `ui/`: **`./freesurfer_test.sh ../pipelines/freesurfer/qc.json all`**.

Paths inside `qc.json` are relative to **`--dataset_dir`**. Use **`[[NIPOPPY_BIDS_PARTICIPANT_ID]]`** and **`[[NIPOPPY_BIDS_SESSION_ID]]`** where filenames include those entities.

This pipeline’s **`qc.json`** uses the same **flat fMRIPrep tree** as **`../fmriprep/qc.json`**: subject-level preproc/mask NIfTIs and `figures/` under **`sample_data/fmriprep/<subject>/`** (see **`ui/freesurfer_test.sh`**, which sets `--dataset_dir` to `sample_data/fmriprep`). There is no separate FreeSurfer or fsQC sample tree in this bundle.

The bundled sample subject **`sub-CMH0001`** ships preproc T1w and brain-mask NIfTIs at the subject root plus recon-all figures under `figures/`.
