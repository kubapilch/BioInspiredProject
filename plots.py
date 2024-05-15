import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

plt.rcParams.update({'font.size': 30})

# Load the data from the CSV file
data = pd.read_csv("validation.csv")

# Filter the data for samples with number of drones equal to 15
filtered_data = data[data["Number of Drones"] == 40]

# Extract attraction constant, repulsion constant, and mean final percentage
attraction_constant = filtered_data["Attraction Constant"]
repulsion_constant = filtered_data["Repulsion Constant"]
mean_final_percentage = filtered_data["Mean Final Percentage"]

# Normalize mean final percentage for color mapping
norm = Normalize(vmin=mean_final_percentage.min(), vmax=mean_final_percentage.max())

# Create a scatter plot with a color gradient
plt.figure(figsize=(10, 8))
scatter = plt.scatter(attraction_constant, repulsion_constant, s=500, c=mean_final_percentage, cmap='spring', norm=norm, alpha=0.7)

# Create a separate colorbar
sm = ScalarMappable(cmap='spring', norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=plt.gca())
cbar.set_label('Mean Final Percentage')

plt.xticks([320, 340, 360, 380])

# Set labels and title
plt.xlabel('Attraction Constant')
plt.ylabel('Repulsion Constant')
# plt.title('20 Drones coverage percentage')

# Show plot
plt.grid(True)
plt.show()
