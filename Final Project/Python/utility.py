import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot(csv_path: str) -> list[list[int]]: 

    # Load the data from a CSV file
    df = pd.read_csv(csv_path)

    # Initialize a 28x28 grid
    grid = np.zeros((28, 28))

    # Normalize function to scale x and y values to 0-27
    def normalize(value, min_val, max_val):
        return 27 * (value - min_val) / (max_val - min_val)

    # Getting the min and max for normalization
    min_x = df['x_pos'].min()
    max_x = df['x_pos'].max()
    min_z = df['z_pos'].min()
    max_z = df['z_pos'].max()

    # Apply normalization
    df['x_pos'] = df['x_pos'].apply(normalize, args=(min_x, max_x))
    df['z_pos'] = df['z_pos'].apply(normalize, args=(min_z, max_z))

    # Populate the grid with z_pos values
    for index, row in df.iterrows():
        x = int(round(row['x_pos']))
        z = int(round(row['z_pos']))
        try:
            grid[z, x] = 1  # Assuming (0,0) is the top-left corner
        except:
            raise Exception("Issue plotting, likely bad indices")

    # Plotting the grid
    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap='viridis', origin='lower')
    plt.colorbar(label='Normalized Z value')
    plt.title('Normalized Plot of Writing on a 28x28 Grid')
    plt.xlabel('Normalized X Position')
    plt.ylabel('Normalized Z Position')
    plt.show()

plot("../Data/A_01.csv")