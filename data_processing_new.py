import os
import pandas as pd

# Function to read data from CSV files and extract relevant information
def process_csv_file(file_path):
    # Extracting information from the file name
    file_name = os.path.basename(file_path)
    parts = file_name.split('-')
    number_of_drones = int(parts[1])
    if parts[2] != "":
        attraction_strength = int(parts[2])
        repulsion_strength = int(parts[3])
    else:
        attraction_strength = int(parts[3])
        repulsion_strength = int(parts[4])
    
    # Reading CSV file
    df = pd.read_csv(file_path, header=None)
    
    # Calculating final percentage and data length
    final_percentage = round(df.iloc[-1, 1] * 100, 2)
    data_length = df.dropna().shape[0]
    
    return [number_of_drones, attraction_strength, repulsion_strength, final_percentage, data_length]

# Path to the folder containing CSV files
folder_path = "csv_results"

# List to store processed data from each file
data = []

# Processing each CSV file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        data.append(process_csv_file(file_path))

# Creating a DataFrame from the processed data
result_df = pd.DataFrame(data, columns=["Number of Drones", "Attraction Constant", "Repulsion Constant", "Final Percentage", "Data Length"])

# Grouping by constants and calculating averages and standard deviations
result_df = result_df.groupby(["Number of Drones", "Attraction Constant", "Repulsion Constant"]).agg({
    "Final Percentage": ["mean", "std"],
    "Data Length": ["mean", "std"]
}).reset_index()

# Rounding floats to two decimal places
result_df = result_df.round(2)

# Renaming columns for clarity
result_df.columns = ["Number of Drones", "Attraction Constant", "Repulsion Constant", 
                     "Mean Final Percentage", "Std Final Percentage", 
                     "Mean Data Length", "Std Data Length"]

# Writing the DataFrame to a CSV file
result_df.to_csv("output.csv", index=False)
