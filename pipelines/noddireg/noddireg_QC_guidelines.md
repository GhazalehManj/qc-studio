# NODDI Registration (noddireg)

**Location (repo sample):** `sample_data/noddireg/<subject>/` — PNGs under `figures/`; subject-level NIfTIs (`*_dwiref.nii.gz`, `*_dseg.nii.gz`) at the subject root. In production, point `--dataset_dir` at your NODDIreg share (same flat layout per subject).

**Review:** PNG figures in `figures/`; use QC-Studio’s parcellation overlay task for the dwiref / dseg Niivue check (ignore `.tsv`, `.txt`, `.pscalar.nii`).

## Purpose

Visually check that NODDI metrics were correctly registered to anatomy and that shared QC images look plausible before consortium release.

## What to review

Each subject folder: `sample_data/noddireg/sub-XXXX/`

Per DWI session, review 6 PNGs under `figures/`:

| File | What it checks |
|------|----------------|
| `figures/*_desc-4S1056Parcels_model-noddi_mdp-icvf_qa.png` | Parcellation alignment on ICVF |
| `figures/*_desc-4S1056Parcels_model-noddi_mdp-od_qa.png` | Parcellation alignment on OD |
| `figures/*_desc-dsegtissue_model-noddi_density.png` | NODDI distributions by CSF / GM / WM |
| `figures/*_icvf_mean_qc.png` | ICVF on cortical surface |
| `figures/*_od_mean_qc.png` | OD on cortical surface |
| `figures/*_isovf_mean_qc.png` | ISOVF on cortical surface |

## Metrics (reference)

| Metric | Meaning |
|--------|---------|
| ICVF | Intracellular volume fraction |
| OD | Orientation dispersion |
| ISOVF | Isotropic volume fraction |

## QC steps (per subject/session)

### Step 1 — Surface QC PNGs

<p align="center"><img src="noddireg_QC_guidelines_assets/surface_qc_example.png" alt="Surface QC example" width="720"></p>

**Files:**

- `figures/sub-XXXX_ses-XX_icvf_mean_qc.png`
- `figures/sub-XXXX_ses-XX_od_mean_qc.png`
- `figures/sub-XXXX_ses-XX_isovf_mean_qc.png`

Each file shows a 2×2 cortical surface rendering of parcel-averaged NODDI values from the 4S1056 atlas.

**Layout:**

- Top left: Left hemisphere, lateral view
- Top right: Left hemisphere, medial view
- Bottom left: Right hemisphere, lateral view
- Bottom right: Right hemisphere, medial view

Color scale shows NODDI values across cortical parcels.

**Check:**

- Smooth, anatomically plausible cortical patterns
- Most of the cortical surface is colored (few large gaps)
- Gradual transitions between regions (no obvious artifact patches)
- ICVF, OD, and ISOVF all look reasonable
- Mild left-right asymmetry is acceptable

**FAIL if:**

- Large holes or missing regions across the cortical surface
- Maps look flat or near-zero across most of cortex
- Obvious artifact patches or extreme discontinuities
- Strong unexplained left-right differences suggesting a processing error

### Step 2 — Parcellation overlay PNGs

<p align="center"><img src="noddireg_QC_guidelines_assets/parcellation_alignment_example.png" alt="Parcellation alignment example" width="720"></p>

**Files (subject root + `figures/`):**

- `sub-XXXX_space-T1w_ref-dwiref_desc-4S1056Parcels_dseg.nii.gz` — 4S1056 parcellation resampled to the DWI reference grid (from noddi_reg)
- `sub-XXXX_ses-XX_*_space-T1w_dwiref.nii.gz` — QSIPrep DWI reference image in T1w space (last DWI session; one file per subject)

We overlay these two images to confirm they are aligned on the DWI reference grid.

**Check:**

The colored parcel labels should sit on brain tissue, follow cortical and subcortical anatomy, and not appear shifted, rotated, or scaled relative to the dwiref background. Parcel boundaries should not extend into ventricles, skull, or background, and expected brain regions should be covered.

**FAIL if:**

- Parcels are clearly shifted from brain tissue, appear in ventricles/skull/background, or large brain areas are missing parcels

<p align="center"><img src="noddireg_QC_guidelines_assets/parcellation_overlay_example.png" alt="Parcellation overlay example" width="720"></p>

**Files (`figures/`):**

- `figures/sub-XXXX_ses-XX_desc-4S1056Parcels_model-noddi_mdp-icvf_qa.png`
- `figures/sub-XXXX_ses-XX_desc-4S1056Parcels_model-noddi_mdp-od_qa.png`

Mosaic slice views showing the 4S1056 parcellation (colored regions) overlaid semi-transparently on the underlying NODDI map.

**Check:**

- Parcels sit on brain tissue and follow anatomy
- No obvious shift, rotation, or scaling error
- Parcel boundaries do not extend into ventricles, skull, or background
- Parcels cover expected brain regions

**FAIL if:**

- Parcels clearly shifted relative to brain tissue
- Parcels visible in ventricles, skull, or background
- Large brain regions missing parcels, or parcels only outside brain

### Step 3 — Tissue density PNG

<p align="center"><img src="noddireg_QC_guidelines_assets/tissue_density_example.png" alt="Tissue density example" width="720"></p>

**File:** `figures/sub-XXXX_ses-XX_desc-dsegtissue_model-noddi_density.png`

This plot checks whether NODDI values look biologically sensible when separated by tissue type (CSF, GM, WM). It does NOT show brain slices. It shows statistical distributions of voxel values.

The plot is built from:

- NODDI maps from AMICO (ICVF, OD, ISOVF)
- Tissue labels from QSIPrep anatomical segmentation (dseg)
- Only voxels with ICVF greater than 0 and less than 0.99 are included (bad or saturated voxels are removed)

**Layout of the figure:** The figure has 3 side-by-side panels — Panel 1: icvf, Panel 2: od, Panel 3: isovf

In each panel there are 3 colored curves (one per tissue):

- CSF (cerebrospinal fluid)
- GM (gray matter)
- WM (white matter)

**Check:**

- **ICVF:** It reflects neurite density and WM peak is to the right of GM; CSF curve is usually separated from brain tissue.
- **OD:** It reflects how spread out fiber directions are within a voxel so tissue curves should be visibly different. Curves should still look like real distributions. Complete overlap across all tissues is suspicious.
- **ISOVF:** It captures free-water-like diffusion. CSF peak is to the right of WM/GM. WM and GM curves are usually lower and closer to each other than CSF. CSF should be clearly separable from brain tissue in most cases.

**FAIL if:**

- CSF, GM, and WM curves overlap almost completely in one or more panels
- ICVF panel shows WM and GM at the same x position with no separation
- ISOVF panel shows CSF not separated from brain tissue
- One curve is mostly a spike at 0 or 1 (suggests masking/fitting problem)
- Curves look flat, empty, or clearly broken
