# Brain-MRI-Tumor-Segmentation-and-Quantitative-Analysis-Pipeline

A Python-based digital image processing application developed for biomedical engineering analysis, focusing on automated tumor localization, comparative threshold segmentation, and quantitative volumetric ratio calculations from Brain Magnetic Resonance Imaging (MRI) data.

## 📋 Project Overview
Manual diagnostics and tracking of pathological anomalies in neuroimaging bring significant subjective inconsistencies and inter-observer error rates. This project establishes an automated, reproducible biomedical imaging pipeline using `OpenCV` and `scikit-image`. Designed to load compressed datasets (`archive.zip`) dynamically, the runtime automatically extracts structural data, thresholds tumor masses via adaptive and Otsu models, isolates boundaries with mathematical morphology, and outputs calculated metric ratios denoting total tumor tissue density.

## 🛠 Technical Pipeline
The workflow standardizes raw brain MRI analysis through a sequential matrix processing pipeline:
1. **Automated Archive Extraction:** Checks for local dataset availability; automatically decompresses structural data paths (`archive.zip`) into distinct tumorous target directories.
2. **Preprocessing (Luminance Isolation):** Converts raw input files to single-channel gray arrays to decouple multi-channel illumination factors, normalizing computation streams.
3. **Comparative Segmentation:**
   * **Otsu’s Automatic Thresholding:** Evaluates global pixel intensity histograms to dynamically compute optimal global thresholds by maximizing inter-class gray-level variances.
   * **Adaptive Gaussian Thresholding:** Calculates dynamic local thresholds over localized pixel neighborhoods to isolate dense tissues under heterogeneous lighting/contrast environments.
4. **Morphological Filtering:** Executes successive Morphological Open operations (`cv2.MORPH_OPEN`) to eradicate weak background structural components while keeping primary pathological shapes intact.
5. **Alpha Overlay Composition:** Generates a colored overlay matrix onto the original image workspace using normalized coefficients (`cv2.addWeighted`), highlighting tumor perimeters via edge-tracing routines (`cv2.findContours`).
6. **Quantitative Biomarker Extraction:** Computes non-zero segmented pixels against the global structural volume to mathematically establish the **Tumor Area Percentage Ratio**.

## 🚀 Key Features
* **Zip File Automation:** Built-in extraction layer that targets and decompresses datasets directly on execution, bypassing manual file restructuring steps.
* **Dual Thresholding Benchmark:** Side-by-side verification comparing Global Otsu adaptive masks with dynamic local thresholds for precise optimization reviews.
* **Mathematical Outlining:** Employs a translucent alpha channel layout bound with hard perimeter outlines to assist visual verification of mass regions.
* **Automated Log Export:** Instantly writes numerical profiles (`results.txt`) and intermediate image matrices (`gray_image.png`, `segmentation_mask.png`, `overlay_result.png`) directly into an organized directory structure (`output_results/`).

## 📂 Project Structure
* `code.py`: Core execution script containing archive manipulation layers, processing pipelines, and analytical engines.
* `output_results/`: Automatically managed folder containing historical processing matrix evaluations and analytical results.
* `report.pdf`: Academic documentation outlining structural mathematical derivations, comparative metric results, and biomedical conclusions.

## 💡 How to Run
1. Verify that your system interpreter environment contains the required package extensions:
   ```bash
   pip install opencv-python numpy matplotlib scikit-image
2. Configure the source dataset system path inside code.py to target your local compressed file:
   ```python
    zip_path = r"C:\path\to\your\archive.zip"
3. Run the processing script:
   ```bash
   python code.py
4. The system will extract the archive, filter target frames, compute segmentations, and launch sequential comparative multi-plot frames. Numerical metrics will show in the console instantly while full logs export into output_results/.

*Developed by Suat AYKURT | Zonguldak Bülent Ecevit University*