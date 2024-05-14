import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from PIL import Image

# Plotting function to visualize the raw position measurements from CSV 
def plot(csv_path: str) -> list[list[int]]: 

    # Load the data from a CSV file
    df = pd.read_csv(csv_path)

    # Initialize a 28x28 grid
    grid = np.zeros((56, 56))

    # Normalize function to scale x and y values to 0-27
    def normalize(value, min_val, max_val):
        return 55 * (value - min_val) / (max_val - min_val)

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

# plot("../Data/A_01.csv")


def csv_to_image(csv_file, image_size=(28, 28)):
  # Initialize empty image with maximum intensity (white)
    image = Image.new("L", image_size, color=0)
    df = pd.read_csv(csv_file, index_col=False)
    df = df[['x_pos', 'z_pos']]
    upsampled = pd.DataFrame()

    upsampled['x_pos'] = (df['x_pos'] + df['x_pos'].shift(1)).dropna() / 2
    upsampled['z_pos'] = (df['z_pos'] + df['z_pos'].shift(1)).dropna() / 2
    # print(upsampled.tail(5))

    df = pd.concat([df, upsampled], axis=0)

    # print(df.tail(5))
    xRange = df['x_pos'].max() - df['x_pos'].min()
    zRange = df['z_pos'].max() - df['z_pos'].min()
    xOffset = 0 
    zOffset = 0 
    if xRange > zRange:
        zOffset = (xRange - zRange) / 2 
    else:
        xOffset = (zRange - xRange) / 2

    buffer = image_size[0] // 5 

    #   xlerp = interpolate.interp1d([int(df['x_pos'].min()), int(df['x_pos'].max()) + 1], [0, 27])
    #   zlerp = interpolate.interp1d([int(df['z_pos'].min()), int(df['z_pos'].max()) + 1], [0, 27])
    xlerp = interpolate.interp1d([(df['x_pos'].min()) - xOffset, (df['x_pos'].max()) + xOffset], [buffer, image_size[0] - buffer])
    zlerp = interpolate.interp1d([(df['z_pos'].min()) - zOffset, (df['z_pos'].max()) + zOffset], [image_size[0] - buffer, buffer])
    
    # Function to draw a line between two points
    def draw_line(x0, y0, x1, y1, size):
        if (x0 - x1) ** 2 + (y0 - y1) ** 2 > size // 5:
            return 
        
        points = []
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

        for x, y in points:
            if 0 <= x < image_size[0] and 0 <= y < image_size[1]:
                image.putpixel((x, y), 255)

    # Iterate over pairs of points and draw lines between them
    for i in range(len(df) - 1):
        x0, y0 = df.iloc[i]
        x1, y1 = df.iloc[i + 1]
        x0 = xlerp(x0)
        y0 = zlerp(y0)
        x1 = xlerp(x1)
        y1 = zlerp(y1)
        draw_line(x0, y0, x1, y1, image_size[0])
    
    return image

# Example usage
# name = "B_01"
# csv_path = "../Data/" + name + ".csv"
# image = csv_to_image(csv_path, (28, 28))

# # Optionally, save the image
# image.save("../Data/Image_" + name + ".png")