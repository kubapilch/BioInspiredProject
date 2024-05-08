import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Load the data from the CSV file
data = pd.read_csv("data_together.csv")

# Filter the data for samples with number of drones equal to 15
filtered_data = data[data["Number of Drones"] == 20]

# Extract attraction constant, repulsion constant, and mean final percentage
attraction_constant = filtered_data["Attraction Constant"]
repulsion_constant = filtered_data["Repulsion Constant"]
mean_final_percentage = filtered_data["Mean Final Percentage"]

# Normalize mean final percentage for color mapping
norm = Normalize(vmin=0, vmax=100)

# Create a scatter plot with a color gradient
plt.figure(figsize=(10, 8))
scatter = plt.scatter(attraction_constant, repulsion_constant, c=mean_final_percentage, cmap='nipy_spectral', norm=norm, alpha=0.7)

# Create a separate colorbar
sm = ScalarMappable(cmap='nipy_spectral', norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=plt.gca())
cbar.set_label('Mean Final Percentage')

# Set labels and title
plt.xlabel('Attraction Constant')
plt.ylabel('Repulsion Constant')
plt.title('20 Drones coverage percentage')

# Show plot
plt.grid(True)
plt.show()
