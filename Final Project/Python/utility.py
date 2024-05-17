import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from PIL import Image

# Function to draw a line between two points on an image
def draw_line(x0, y0, x1, y1, size, image):
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
        if 0 <= x < size and 0 <= y < size:
            image.putpixel((x, y), 255)

def points_to_image(position_points, image_size=(28, 28)):

    # Initialize empty image with maximum intensity (white)
    image = Image.new("L", image_size, color=0)

    # scales the dataframe to the desired frame size 
    x_range = position_points['x_pos'].max() - position_points['x_pos'].min()
    z_range = position_points['z_pos'].max() - position_points['z_pos'].min()
    x_offset, z_offset = 0, 0
    buffer = image_size[0] // 5 
    
    if x_range > z_range:
        z_offset = (x_range - z_range) / 2 
    else:
        x_offset = (z_range - x_range) / 2

    xlerp = interpolate.interp1d([(position_points['x_pos'].min()) - x_offset, (position_points['x_pos'].max()) + x_offset], [buffer, image_size[0] - buffer])
    zlerp = interpolate.interp1d([(position_points['z_pos'].min()) - z_offset, (position_points['z_pos'].max()) + z_offset], [image_size[0] - buffer, buffer])
    
    # Iterate over pairs of points and draw lines between them
    for i in range(len(position_points) - 1):
        x0, y0 = position_points.iloc[i]
        x1, y1 = position_points.iloc[i + 1]
        x0 = xlerp(x0)
        y0 = zlerp(y0)
        x1 = xlerp(x1)
        y1 = zlerp(y1)
        draw_line(x0, y0, x1, y1, image_size[0], image)
    
    return image
