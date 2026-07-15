# Tumor Spheroid Growth-Induced Pressure Pipeline

This repository contains the full experimental-computational pipeline used to quantify growth-induced pressure exerted by tumor spheroids embedded in constraining hydrogels. The pipeline takes raw time-lapse microscopy images through registration, bead tracking, displacement correction, and finite-element-based pressure derivation.

## Pipeline Overview

```
1. FEA Lookup Table (ABAQUS)         →  Run once per material/gel condition
2. 8-bit Conversion (Fiji macro)     →  8bit.ijm
3. Image Registration                →  img_reg.py
4. Point Selection / Bead Tracking   →  select_point.py
5. Displacement Correction           →  correct_maker.py
6. Pressure Derivation                →  pressure_calculation.py
```

Steps 2–6 are run once per time point per sample. Step 1 (the FEA simulation database) is a shared lookup table built once per material condition and reused across all samples of that condition.

---

## 0. Prerequisites / Setup

**Software required:**
- [Fiji/ImageJ](https://fiji.sc/) — for `.czi` → 8-bit `.tif` conversion
- Python 3.9+
- Spyder (recommended IDE): `pip install spyder`
- Required Python libraries:
  ```
  pip install numpy pandas matplotlib opencv-python imageio scikit-image
  ```
- Abaqus/CAE 2022 (or compatible) — for the FEA lookup table simulations

**Recommended folder structure per sample**, matching what the scripts expect:
```
/<sample>/
  raw/          # original .czi files
  8bit/         # 8-bit .tif output from 8bit.ijm
  align/        # registered images from img_reg.py (0ref.tif, <t>h.tif, ...)
  points/       # manually selected keypoint Excel files from select_point.py
  correct/      # corrected displacement Excel files from correct_maker.py
  pressure/     # final pressure output from pressure_calculation.py
```

---

## 1. FEA Lookup Table (ABAQUS)

**Purpose:** Generates a database of simulated normalized bead displacement–distance curves across a swept range of applied pressures (0.1–100 Pa, in 0.1 Pa increments). This database is later used as the reference lookup table that experimental displacement data is matched against (Step 6).

**Script:** ABAQUS/CAE Python replay script (e.g. `abaqus_yeoh_<condition>.py`)

**What it does:**
- Builds a 2D axisymmetric quarter-section model of the spheroid-in-gel geometry.
- Assigns a **Yeoh hyperelastic material model** parameterized from the AFM-measured elastic modulus (E) of the specific gel condition being modeled (see Material Model Notes below).
- Applies a uniform pressure load to the inner (spheroid) boundary, sweeping across the full pressure range.
- Extracts node displacements along the outer boundary and writes them to `uv_data<pressure>.csv` files (one per pressure value), which populate the simulation folder used by `pressure_calculation.py`.

**⚠️ Material model must be updated per gel condition.** The Yeoh parameters (C10, C20, C30, D1) are specific to the elastic modulus (E) and Poisson's ratio (ν) of the gel being modeled. **Do not reuse parameters across different agarose concentrations** — recompute from the measured E for each new condition using:

```
C10 = E / 6
C20 = -0.1 * C10
C30 = 0.01 * C10
D1  = 6 * (1 - 2*ν) / E
```

---

## 2. 8-bit Conversion — `8bit.ijm`

**Purpose:** Converts raw `.czi` microscopy files to 8-bit grayscale `.tif`, required for compatibility with all downstream Python scripts.

**Software:** Fiji/ImageJ (macro)

**Usage:**
1. Open Fiji, go to `Plugins > Macros > Run...`
2. Select `8bit.ijm`
3. Choose the source directory (containing `.czi` files) and destination directory
4. The macro opens each `.czi` file, converts it to 8-bit, and saves it as `.tif` in the destination folder

---

## 3. Image Registration — `img_reg.py`

**Purpose:** Aligns each time-point image to a fixed 0-hour reference image, correcting for translational and rotational drift introduced by stage repositioning or sample handling on the custom live-imaging setup.

**Method:** ORB (Oriented FAST and Rotated BRIEF) feature detection and matching.
1. Contrast is enhanced via CLAHE (clip limit 5.0, tile size 8×8) on both images.
2. A central mask excludes the spheroid itself from feature detection, so registration is driven by the surrounding (stationary) bead field rather than the growing tumor.
3. ORB keypoints are detected and matched via brute-force Hamming matching.
4. A partial affine transform (translation + rotation + uniform scale) is estimated from the matches and applied to align the moving image to the reference.
5. Both images are cropped to a shared region of interest (user-defined crop ratio, typically 0.1) to remove registration edge artifacts.

**Inputs:** Reference image path, moving image path, output directory, crop ratio (0–0.99)
**Output:** `aligned_and_cropped.tif`

**Note:** Make sure input images are already 8-bit `.tif` files from Step 2.

---

## 4. Point Selection / Bead Tracking — `select_point.py`

**Purpose:** Manually select matching bead pairs between the reference and registered moving image, forming the raw displacement dataset for correction and pressure derivation.

**Method:**
1. Images are resized, contrast-enhanced, and masked to assist visual bead identification.
2. The largest contour (spheroid boundary) is detected and its centroid computed, for reference during selection.
3. An interactive dual-window interface lets the user click matching bead pairs — left-click to select, right-click to remove.
4. For each click, the script snaps to the local minimum-intensity pixel within a small window, improving click precision (the algorithm auto-refines an imprecise manual click to the true darkest point of the bead).

**Recommended:** Select at least 100 matching pairs per image pair. Ensure equal numbers of points are selected in both images, or the output will not save.

**Output:** Excel file with columns `Match Index`, `x1, y1` (reference coordinates), `x2, y2` (moving coordinates).

---

## 5. Displacement Correction — `correct_maker.py`

**Purpose:** Corrects raw bead displacement by projecting it onto the true local surface normal of the tumor boundary — rather than assuming displacement is purely radial from the centroid — accounting for the fact that spheroids are not perfectly circular.

**Method:**
1. The tumor boundary is segmented via Otsu thresholding (global) and its contour extracted.
2. For each bead, a **local second-order polynomial** is fit to nearby contour points (within `angle_half_range` degrees of the bead's angular position relative to the centroid), providing a smooth local approximation of the boundary.
3. The tangent slope is computed analytically from the polynomial's derivative at the intersection point; the normal is perpendicular to this tangent.
4. The raw displacement vector (reference point → moving point) is projected onto this local normal direction to give the corrected displacement component.

**Two variants:**
| Script | Thresholding method | Use case |
|---|---|---|
| `correct_maker.py` | Global Otsu threshold | Standard images with uniform illumination |
| `correct_maker_badcontrast.py` | **Local adaptive threshold** (`threshold_local`, block size 51) | Images with uneven illumination / poor global contrast, where a single global threshold under- or over-segments the boundary |

**Interactive tuning:** The script displays the segmentation mask and tangent/secant line visualization, prompting the user to accept or adjust the `threshold` and `angle_half_range` parameters (default 10°) before finalizing.

**Inputs:** Reference image path (post-registration), keypoint Excel file (from Step 4), output path, threshold, angle_half_range
**Outputs:**
- Excel file with `c_dist` (normalized centroid-to-bead distance), `c_disp` (normalized corrected displacement), `r` (raw radius)
- `*_radius_vs_angle.png` — boundary shape profile
- Visualization plots: mask + centroid, tangent/secant lines, projection of moving points onto normals

---

## 6. Pressure Derivation — `pressure_calculation.py`

**Purpose:** Matches the corrected experimental displacement–distance data against the FEA simulation database (Step 1) to estimate the growth-induced pressure that best explains the observed matrix deformation.

**Interface:** Tkinter GUI (no manual code editing required).

**Method:**
1. Loads all `uv_data<pressure>.csv` files from the specified simulation folder (0.1–100 Pa sweep).
2. Fits a 4th-degree polynomial to each simulated pressure's displacement–distance curve.
3. Loads the corrected experimental data (`c_dist`, `c_disp`) from Step 5's output.
4. For each candidate pressure, evaluates the fitted polynomial at the experimental distances and computes the sum of squared errors (SSE) against the experimental displacement.
5. Selects the pressure with minimum SSE as the best-fit pressure.

**Inputs (via GUI):**
- Simulation folder (containing `uv_data*.csv` — **must match the correct gel condition/radius**, see tip below)
- Corrected Excel file (from Step 5)
- Sheet index (usually 0)
- Radius range (`r_low`, `r_high`) to restrict analysis to a specific shell distance from the spheroid
- Output file path

**Tip:** When selecting the simulation folder, use the one matching the sample's actual radius (e.g., a spheroid with r ≈ 154 µm should use the `154` simulation folder, not an arbitrary one) — the geometry the FEA model was built with should match the experimental spheroid size being analyzed.

**Outputs:**
- Excel file: `dist`, `c_disp` (experimental), `dispFEM` (best-fit simulated), `r`, `pressure` (best-fit value, repeated per row)
- Plot: experimental vs. FEM displacement scatter/line comparison, with best-fit pressure in the title
- Console: best-fit pressure and SSE

---

## Key Algorithmic Notes

- **CLAHE contrast enhancement** (clip limit 5.0, 8×8 tiles) is used in both registration and bead selection steps to improve feature visibility under the brightness variability typical of the custom, non-commercial live-imaging setup.
- **ORB was chosen over simpler translation-only methods** (e.g., phase correlation) because the imaging setup can introduce combined rotational and translational drift; phase correlation cannot resolve rotation and is unsuitable here.
- **Centroid-normal correction (Step 5)** exists because tumor spheroids deviate from perfect circularity; using the local contour-derived normal, rather than the naive centroid-to-bead radial direction, gives a more physically accurate displacement component aligned with the true local stress direction.

---

## Known Limitations

- The FEA Yeoh material model's C2 and C3 parameters are set via a fixed heuristic ratio (C2 = −0.1×C1, C3 = 0.01×C1) rather than independently fit to large-strain data, since AFM indentation only measures the small-strain modulus. Absolute pressure values derived from this pipeline should be treated as a bounded estimate rather than an exact measurement (see dissertation Section 6.3.6/6.3.7 for full discussion).
- Displacement correction (Step 5) assumes the spheroid boundary is well-approximated by a local 2nd-order polynomial; highly irregular or lobed boundaries may require a smaller `angle_half_range` for accurate local fitting.
