import os
import numpy as np
from tqdm.notebook import tqdm
import pandas as pd
from scipy import stats

# normalize the Hr data
from sklearn.preprocessing import MinMaxScaler

# create a directory to store the generated files
try:
    os.makedirs("../generated_data/train/", exist_ok=True)
    os.makedirs("../generated_data/test/", exist_ok=True)
    
    os.makedirs("../generated_data/train/Hr", exist_ok=True)
    os.makedirs("../generated_data/test/Hr", exist_ok=True)
    
    os.makedirs("../generated_data/train/HaHb", exist_ok=True)
    os.makedirs("../generated_data/test/HaHb", exist_ok=True)
    print("Directory created successfully or already exists.")
except Exception as e:
    print(f"Error creating directory: {e}")


def get_HaHb_array(data,hydropathy_scale):
    HaHb_list = []
    # For one scale get all HaHb values
    # iterate over the dataset
    for i in range(data.shape[0]):
        row = data.iloc[i]
        resA_ = row['resA']
        resB_ = row['resB']
        resB_1 = row['resB_1']
        resB_2 = row['resB_2']
        resB_3 = row['resB_3']
        resB_4 = row['resB_4']
        resB_5 = row['resB_5']
        resB_6 = row['resB_6']
        resB_7 = row['resB_7']
        resB_8 = row['resB_8']
        resB_9 = row['resB_9']

        # get values from the scale
        resA_scale_value = hydropathy_scale[resA_].iloc[0]
        resB_scale_value = hydropathy_scale[resB_].iloc[0]
        resB_1_scale_value = hydropathy_scale[resB_1].iloc[0]
        resB_2_scale_value = hydropathy_scale[resB_2].iloc[0]
        resB_3_scale_value = hydropathy_scale[resB_3].iloc[0]
        resB_4_scale_value = hydropathy_scale[resB_4].iloc[0]
        resB_5_scale_value = hydropathy_scale[resB_5].iloc[0]
        resB_6_scale_value = hydropathy_scale[resB_6].iloc[0]
        resB_7_scale_value = hydropathy_scale[resB_7].iloc[0]
        resB_8_scale_value = hydropathy_scale[resB_8].iloc[0]
        resB_9_scale_value = hydropathy_scale[resB_9].iloc[0]

        # calculate HaHb values
        currentcombination = [resA_scale_value*resB_scale_value, 
        resA_scale_value*resB_1_scale_value, 
        resA_scale_value*resB_2_scale_value, 
        resA_scale_value*resB_3_scale_value, 
        resA_scale_value*resB_4_scale_value, 
        resA_scale_value*resB_5_scale_value, 
        resA_scale_value*resB_6_scale_value, 
        resA_scale_value*resB_7_scale_value, 
        resA_scale_value*resB_8_scale_value, 
        resA_scale_value*resB_9_scale_value]

        HaHb_list.append(currentcombination)
    return np.array(HaHb_list)

def get_values_for_abc(HaHb_min,HaHb_max,HaHb_median):
    x1 = HaHb_min
    x2 = HaHb_max
    x3 = HaHb_median
    A = np.array([
        [-x1**2, x1, 1],
        [-x2**2, x2, 1],
        [-x3**2, x3, 1]
    ])
    
    # Constants matrix
    B = np.array([0, 0, 1])
    
    # Solving the system of equations
    solution = np.linalg.solve(A, B)
    a, b, c = solution
    # print(a,b,c)
    return a,b,c

# using the formula
"""def get_values_for_abc(HaHb_max,HaHb_min,HaHb_median):
    x1 = HaHb_min
    x2 = HaHb_max
    x3 = HaHb_median

    a = -1 / (x1 * x2 - x1 * x3 - x2 * x3 + x3**2)
    b = (- (x1 + x2)) / (x1 * x2 - x1 * x3 - x2 * x3 + x3**2)
    c = (x1 * x2) / (x1 * x2 - x1 * x3 - x2 * x3 + x3**2)
    return a,b,c"""

# read the main dataset
filename = "../dataset/train/dataset.txt"
dataset = pd.read_csv(filename)

# drop the pdb column
data = dataset.drop(columns=['pdb'], axis=1)

# read the test dataset
# read the main dataset
filename = "../dataset/test/dataset.txt"
dataset_test = pd.read_csv(filename)

# drop the pdb column
data_test = dataset.drop(columns=['pdb'], axis=1)
print(data_test.shape)
data_test.head()

# to calcula a,b,c values
data_combined = pd.concat([data, data_test], axis=0)
print(data_combined.shape)
data_combined.head()

# loop through hydropathy folder and pick scale one by one, generate HaHb values and save them in a list
# iterate over the directory
directory = "../hydropathy/"

# Initialize the MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

for file_path in tqdm(os.listdir(directory)):

    # ----------------------------------------------------------------------------
    # calculate HaHb
    # final list to save the HaHb values


    hydropathy_scale = pd.read_csv(directory + file_path,header = None)
    hydropathy_scale.columns = ['aa', 'hydropathy']

    # typecast hydropathy values to float
    hydropathy_scale['hydropathy'] = hydropathy_scale['hydropathy'].astype(float)

    hydropathy_scale = hydropathy_scale.T
    # make first row as header
    new_header = hydropathy_scale.iloc[0]
    hydropathy_scale = hydropathy_scale[1:]
    hydropathy_scale.columns = new_header
    hydropathy_scale.reset_index(drop=True, inplace=True)

    # for training data
    HaHb_train = get_HaHb_array(data,hydropathy_scale)

    # for test data
    HaHb_test = get_HaHb_array(data_test,hydropathy_scale)

    # for a,b,c calculation
    HaHb_combined = get_HaHb_array(data_combined,hydropathy_scale)
    #print(HaHb.shape)
    
    # apply log transformation on HaHb_combined
    #HaHb_combined = np.log(HaHb_combined)

    # get mid,min and max values of HaHb
    HaHb_min = np.min(HaHb_combined)
    HaHb_max = np.max(HaHb_combined)
    HaHb_median = np.median(HaHb_combined)
    #print(HaHb_median)

    # ----------------------------------------------------------------------------
    #print(HaHb.shape)
    # calculate Hr
    try:
        # pre normalization
        a, b, c = get_values_for_abc(HaHb_max, HaHb_min, HaHb_median)
        
        # saving value to print later
        a_, b_, c_ = get_values_for_abc(HaHb_max, HaHb_min, HaHb_median)
        
        # post normalization
        #a,b,c = round(a/4,3),round(b/4,3),round(c/4,3)
        #print("after normalizaion",a,b,c)

    except np.linalg.LinAlgError as e:
        print(f"Processing file: {directory+file_path}")
        print(f"Error calculating values for a, b, c: {e}")
        print("Skipping this iteration due to singular matrix.")
        #print(HaHb)
        continue
    
    # get Hr values
    Hr_train = np.array(list(map(lambda HaHb_train: (-a * (HaHb_train ** 2)) + ((b * HaHb_train) + c), HaHb_train.flatten()))).reshape(HaHb_train.shape)
    Hr_test = np.array(list(map(lambda HaHb_test: (-a * (HaHb_test ** 2)) + ((b * HaHb_test) + c), HaHb_test.flatten()))).reshape(HaHb_test.shape)

    # normalize the Hr values
    Hr_train_norm = scaler.fit_transform(Hr_train)
    Hr_test_norm = scaler.fit_transform(Hr_test)

    # save train hr files
    file_name = file_path.replace('.csv', '')
    np.savetxt(f"../generated_data/train/HaHb/{file_name}.txt", HaHb_train)
    np.savetxt(f"../generated_data/train/Hr/{file_name}.txt", Hr_train_norm)
    # save test hr files
    np.savetxt(f"../generated_data/test/HaHb/{file_name}.txt", HaHb_test)
    np.savetxt(f"../generated_data/test/Hr/{file_name}.txt", Hr_test_norm)
    
    #print("________________________________")
    