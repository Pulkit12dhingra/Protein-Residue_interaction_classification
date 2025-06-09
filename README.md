# Protein Interaction Classification 

## Problem Statement

Given protein structure data, the objective is to predict whether a pair of residues interact, using deep learning and engineered features (including hydropathy scales).

---

## Repository Structure

- `codes/` – Python scripts for feature generation and model training
- `dataset/` – Raw and processed data (train/test splits, features, labels)
- `generated_data/` – Feature files generated for each hydropathy scale
- `hydropathy/` – Hydropathy scale CSV files
- `models/` – Saved model files
- `notebooks/` – Jupyter notebooks for data processing, model training, and analysis
- `static/` – Output plots and result CSVs
- `requirements.txt` – Python dependencies

---

## Python Environment Setup Guide

Follow these steps to set up your Python environment for this project.

### Prerequisites

- **Python 3.12+** (tested on Python 3.12.7)

### Steps to Set Up the Environment

1. **Create a Virtual Environment**  
   ```bash
   python -m venv <env_name>
   ```
   Replace `<env_name>` with your preferred environment name.  
   *Tip: Keep the environment folder out of your Git repository.*

2. **Activate the Virtual Environment**  
   - On macOS/Linux:  
     ```bash
     source <env_name>/bin/activate
     ```
   - On Windows:  
     ```bash
     .\<env_name>\Scripts\activate
     ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
   **Important:** Do not modify the version numbers in `requirements.txt`.

4. **Deactivate the Environment**  
   ```bash
   deactivate
   ```

---

## How to Use

- Run and explore the Jupyter notebooks in the `notebooks/` directory for data processing, feature engineering, model training, and evaluation.
- Use scripts in `codes/` for batch processing or model runs.
- Results and plots are saved in the `static/` directory.

---

## Team

- Shaivya Shankar
- Pulkit Dhingra
- Luoxi Liu
- Shuyi Li
