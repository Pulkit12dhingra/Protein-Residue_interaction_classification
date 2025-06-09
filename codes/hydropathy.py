"""
Filename: hr_generate.py
Function: Used to generate multiple HR files based on hydrogen affinity data
Date: 2024-02-13
Description:
- Traverse the CSV files in the hydropathy folder
- Calculate the ab parameter values ​​specific to each scale
- Read the dataset.txt data and calculate the HR value
- Save the calculation results to the output_hr folder
"""
import os
import pandas as pd
import itertools

def compute_ab(hydropathy_values):
    """Compute a and b for each scale"""
    products = [ha * hb for ha, hb in itertools.combinations_with_replacement(hydropathy_values.values(), 2)]
    max_HA_HB = max(products)
    a = 4 / (max_HA_HB ** 2)
    b = 4 / max_HA_HB
    print(f"Computed parameters: a={a}, b={b}")
    return a, b

def generate_hr_file(hydropathy_file, dataset_file, output_file):
    """According the scales in hydropathy and resA/resB in dataset.txt to compute hr.txt"""
    hydropathy_df = pd.read_csv(hydropathy_file, header=None, names=["AminoAcid", "Hydropathy"])
    hydropathy_dict = dict(zip(hydropathy_df["AminoAcid"], hydropathy_df["Hydropathy"]))
    
    a, b = compute_ab(hydropathy_dict)
    
    with open(dataset_file, "r") as f:
        lines = f.readlines()
    
    header = lines[0].strip().split(",")
    data_lines = lines[1:]
    
    with open(output_file, "w") as f_out:
        for line in data_lines:
            parts = line.strip().split(",")
            resA = parts[1]
            resB_list = parts[2:]
            
            hr_values = []
            for resB in resB_list:
                if resA in hydropathy_dict and resB in hydropathy_dict:
                    HA_HB = hydropathy_dict[resA] * hydropathy_dict[resB]
                    Hr = -a * (HA_HB ** 2) + b * HA_HB
                else:
                    Hr = 0  # if none
                hr_values.append(str(Hr))
            
            f_out.write(" ".join(hr_values) + "\n")

def process_all_hydropathy_files(hydro_folder, dataset_file, output_folder):
    """Traverse the hydropathy folder and generate multiple hr.txt"""
    os.makedirs(output_folder, exist_ok=True)
    
    for hydro_file in os.listdir(hydro_folder):
        if hydro_file.endswith(".csv"):
            hydro_path = os.path.join(hydro_folder, hydro_file)
            output_path = os.path.join(output_folder, f"hr_{os.path.splitext(hydro_file)[0]}.txt")
            print(f"Processing: {hydro_file} -> {output_path}")
            generate_hr_file(hydro_path, dataset_file, output_path)

# Define the file path
hydropathy_folder = "./hydropathy"
dataset_path = "./dataset/train/dataset.txt"
output_hr_folder = "./datatset_new/train"
process_all_hydropathy_files(hydropathy_folder, dataset_path, output_hr_folder)

hydropathy_folder = "./hydropathy"
dataset_path = "./dataset/test/dataset.txt"
output_hr_folder = "./datatset_new/test"
process_all_hydropathy_files(hydropathy_folder, dataset_path, output_hr_folder)