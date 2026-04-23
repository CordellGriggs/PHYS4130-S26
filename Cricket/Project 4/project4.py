'''
Filename: project4.py
Written by: Cricket Bergner
Date: 04/22/2026
'''

# import libraries
import numpy as np
from matplotlib import pyplot as plt
import random as ra
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# important functions

# calculated capacity dimension for different DLA functions
def calculate_capacity_dimension(grid):
    # calculates the Minkowski-Bouligand (box-counting) dimension
    pixels = np.argwhere(grid > 0)
    if len(pixels) < 2: return 0
    
    # Determine the maximum possible box size based on grid shape
    max_side = max(grid.shape)
    scales = np.unique(np.floor(np.logspace(0, np.log10(max_side / 2), 15)).astype(int))
    scales = scales[scales > 1]
    ns = []
    
    for s in scales:
        bins = (pixels // s).astype(int)
        unique_bins = np.unique(bins, axis=0)
        ns.append(len(unique_bins))
    
    # linear regression
    coeffs = np.polyfit(np.log(scales), np.log(ns), 1)
    return -coeffs[0]

# for 2D DLA, particle wandering
def move_2D(px, py): 
    direction = ra.randint(0, 3)
    if direction == 0: py += 1
    elif direction == 1: py -= 1
    elif direction == 2: px -= 1
    elif direction == 3: px += 1
    return px, py

# for 2D Triangular DLA, particle wandering
def move_2Dt(px, py):
    direction = ra.randint(0, 5)
    if direction == 0: px += 1
    elif direction == 1: px -= 1
    elif direction == 2: py += 1
    elif direction == 3: py -= 1
    elif direction == 4:
        py += 1
        px += (1 if py % 2 != 0 else -1)
    elif direction == 5:
        py -= 1
        px += (1 if py % 2 != 0 else -1)
    return px, py

# for 3D DLA, particle wandering
def move_3D(px, py, pz):
    d = ra.randint(0, 5)
    if d == 0: px += 1
    elif d == 1: px -= 1
    elif d == 2: py += 1
    elif d == 3: py -= 1
    elif d == 4: pz += 1
    elif d == 5: pz -= 1
    return px, py, pz

# if particle nears another particle, it sticks
def sticking(px, py, grid, stickiness):
    if np.any(grid[px-1:px+2, py-1:py+2] > 0):
        return ra.random() <= stickiness
    return False

# if particle nears another particle, it sticks (DLA 2D triangular)
def sticking_2Dt(px, py, grid, stickiness, n):
    dx = 1 if py % 2 != 0 else -1
    neighbors = [(px+1, py), (px-1, py), (px, py+1), (px, py-1),
                 (px+dx, py+1), (px+dx, py-1)]
    for i, j in neighbors:
        if 0 <= i < n and 0 <= j < n and grid[i, j] > 0:
            return ra.random() <= stickiness
    return False

