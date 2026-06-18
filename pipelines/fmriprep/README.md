# fMRIPrep QC configuration

QC-Studio loads **only** `qc.json` from this folder. Run `streamlit run ui/main.py …` from the repository root, or use **`fmriprep_demo.sh`** (repo root) / **`ui/fmriprep_test.sh`** (from `ui/`) for the same defaults.

Example (after `cd` to the qc-studio root):

```bash
streamlit run ui/main.py --server.port=8501 -- \
  --qc_json ../pipelines/fmriprep/qc.json \
  --qc_task anat_wf_qc \
  --qc_pipeline fmriprep \
  --dataset_dir sample_data \
  --participant_list sample_data/qc_participants.tsv \
  --session_list ses-01,ses-02 \
  --output_dir ./output
```

Use **`--session_list`** with comma-separated BIDS session labels (e.g. `ses-01,ses-02`). The app builds one review **page** per **(participant × session)** from your participant list. If `qc_participants.tsv` includes a **`session_id`** column, that file defines the exact rows instead (one row per participant–session pair).

### Multiple tasks in `qc.json` (`anat_wf_qc`, `sdc_wf_qc`, `coreg_wf_qc`, …)

`qc.json` can define **several** tasks. You choose how to run QC-Studio:

- **One task per run** (default): pass the task key with **`--qc_task`** (e.g. `anat_wf_qc`). The UI does not switch tasks mid-session.
- **All tasks on one scrollable page**: use **`--qc_task all`**. Each cohort page gets a PASS / FAIL / UNCERTAIN (and notes) **per task**, and the sidebar marks a page complete only when **every** task in `qc.json` has a decided rating.

Examples:

- From repo root with **`fmriprep_demo.sh`**: set **`QC_TASK`** (default `anat_wf_qc`), e.g. `QC_TASK=sdc_wf_qc ./fmriprep_demo.sh`, or `QC_TASK=all …` for every task on one page.
- From `ui/` with **`fmriprep_test.sh`**: use **`QC_TASK`**, or pass the task as the **second** argument after `qc.json`, e.g. `./fmriprep_test.sh ../pipelines/fmriprep/qc.json coreg_wf_qc`, or `./fmriprep_test.sh ../pipelines/fmriprep/qc.json all`.

Paths inside `qc.json` are relative to **`--dataset_dir`**. Use the **`[[NIPOPPY_BIDS_PARTICIPANT_ID]]`** and **`[[NIPOPPY_BIDS_SESSION_ID]]`** placeholders where filenames include those entities.

The **3D Niivue panel** needs `base_mri_image_path` in each task. The bundled config uses flat layout under **`sample_data/fmriprep/<subject>/`**: BIDS NIfTIs in `bids/`, figures in `figures/`, and subject-level preproc/mask NIfTIs at the subject root. Shipped **`sub-CMH0001`** BOLD files are **first-volume-only** (full runs exceed GitHub’s file-size limit). A small demo subject **`sub-ED01`** remains under **`sample_data/derivatives/fmriprep/`** (legacy layout).

The FreeSurfer pipeline **`../freesurfer/qc.json`** uses the same flat layout under **`sample_data/fmriprep/<subject>/`** (subject-level preproc/mask NIfTIs and `figures/`).
