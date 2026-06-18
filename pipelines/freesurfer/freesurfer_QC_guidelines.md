# FreeSurfer QC

## Quick reference

| Rating | When to use |
|--------|-------------|
| **PASS** | Red and blue outlines follow brain anatomy; no major cortex missing; cerebellum may be partly excluded |
| **FAIL** | Major cortex excluded, outlines in skull, or segmentation clearly wrong |
| **UNCERTAIN** | Borderline case — flag for supervisor review |

**In the app:** Open each participant × session, review the recon-all figure (red = outer brain boundary, blue = white matter), check all axes, then rate.

**Sample data:** `sample_data/fmriprep/<subject>/figures/` (same tree as fMRIPrep; see `pipelines/freesurfer/qc.json`).

---

## 1. What you are checking

FreeSurfer reconstructs cortex from a T1w scan. Your job is to confirm the **red** (brain/skull-stripped boundary) and **blue** (white matter) outlines look correct — not to catch every tiny flaw.

Small imperfections are normal. Fail only when errors would likely affect downstream analysis.

---

## 2. Outlines — what they mean

| Outline | Meaning | Fail if… |
|---------|---------|----------|
| **Red** | Outer brain boundary (skull strip) | Major cortex missing, or line runs into skull |
| **Blue** | White matter boundary | Major WM missing, or line runs into skull / non-brain tissue |

**Cerebellum:** The red outline should follow cortex and **may exclude** cerebellum. Missing cerebellum from the outline can still **PASS**.

Always view **all axes** before rating — some problems show in only one view.

---

## 3. Good example

<img src="freesurfer_QC_guidelines_assets/good_example.png" alt="Good FreeSurfer segmentation: red brain outline and blue white-matter outline" width="720">

*Red traces the brain boundary; blue traces white matter. No skull in the outlines; cerebellum excluded.*

**→ PASS**

---

## 4. Common issues

### Over-inclusive masking (skull visible in image)

Skull may appear in the background. This is **not** an automatic fail — only fail if the **red or blue outline extends into skull**.

<img src="freesurfer_QC_guidelines_assets/over_inclusive_masking.png" alt="Skull visible around brain — check whether outlines cross into skull" width="720">

---

### Underexclusive masking (cortex missing from outline)

Major parts of cortex excluded from the red outline → **FAIL**.

<img src="freesurfer_QC_guidelines_assets/underexclusive_masking_1.png" alt="Underexclusive masking example 1 — frontal cortex excluded" width="360">
<img src="freesurfer_QC_guidelines_assets/underexclusive_masking_2.png" alt="Underexclusive masking example 2 — cortex excluded from outline" width="360">

---

### Temporal lobe excluded

Check all axes. Major temporal-lobe exclusion → **FAIL** or **UNCERTAIN**.

<img src="freesurfer_QC_guidelines_assets/temporal_lobe_excluded.png" alt="Temporal lobe excluded from cortical outline" width="360">

---

### Missing cerebellum from outline

Can still **PASS** if cortex is otherwise fine.

<img src="freesurfer_QC_guidelines_assets/missing_cerebellum_pass.png" alt="Cerebellum partly outside red outline — acceptable" width="720">

---

### Minor skull in background

Fail only if outlines cross into skull.

<img src="freesurfer_QC_guidelines_assets/minor_skull_1.png" alt="Minor skull visible — outlines still on brain" width="360">
<img src="freesurfer_QC_guidelines_assets/minor_skull_2.png" alt="Minor skull visible — second view" width="360">

---

### Minor cerebellum inclusion

Outline slightly into cerebellum → usually **not FAIL**, but note it (e.g. slices x=17, x=−16, y=−62).

<img src="freesurfer_QC_guidelines_assets/minor_cerebellum.png" alt="Outline slightly extends into cerebellum" width="720">

---

### Missing red or blue outline

Cannot judge segmentation properly → **UNCERTAIN** or **FAIL**.

<img src="freesurfer_QC_guidelines_assets/missing_outline.png" alt="Missing red or blue segmentation outline" width="720">

---

## 5. Euler values

Euler numbers are shown in the app (typical range **−150 to 2**).

- Use Euler as **one signal**, not the only rule.
- Do **not** fail on Euler alone if the segmentation looks good visually.
- Study-wide Euler distributions may inform final decisions.
