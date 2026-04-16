# file for commit updates

# original draft 1 section of code

'''
Filename: P4D1
Written by: Cricket Bergner
Date: 04/07/26
'''

# import libraries
import numpy as np
from matplotlib import pyplot as plt
import random as ra

# functions
def move(px,py):

  # the aimless wandering
  direction = ra.randint(0, 3)
  if direction == 0:
    py += 1
  elif direction == 1:
    py -= 1
  elif direction == 2:
    px -= 1
  elif direction == 3:
    px += 1

  return px, py

# def sticking(px, py, grid, stickiness): # works but is slower
#     neighbors = [(px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)]

#     for nx, ny in neighbors:
#         if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]: # making sure nothing is out of bounds
#             if grid[nx, ny] > 0:
#                 if ra.random() <= stickiness:
#                     return True  # if the random number is less that the stickiness factor, then it sticks

#     return False

def sticking(px, py, grid, stickiness):
    # check a 3x3 square around the particle to see where the neighbors are
    if np.any(grid[px-1:px+2, py-1:py+2] > 0):
        if ra.random() <= stickiness:
            return True
    return False

# initial variables
n = 100
stickiness = 0.9
grid = np.zeros((n, n)) # n by n grid
num_p = 100
r_max = 0

center = n // 2 # establishing center of the grid
grid[center, center] = 1

spawn = n // 2 - 10
delete = n // 2 + 2 # border for particles

for i in range(num_p):

    # spawn new particle
    theta = ra.uniform(0, 2 * np.pi) # angle from center
    px = int(center + spawn * np.cos(theta)) # polar coordinates
    py = int(center + spawn * np.sin(theta))

    stuck = False
    while not stuck:
        px, py = move(px, py)

        # when particle leaves the circle, respawn it
        if px < 0 or px >= n or py < 0 or py >= n:
            theta = ra.uniform(0, 2 * np.pi)
            px = int(center + spawn * np.cos(theta))
            py = int(center + spawn * np.sin(theta))
            continue

        # what if the particle hits the border
        dx, dy = px - center, py - center
        if (dx**2 + dy**2) > delete**2:
            theta = ra.uniform(0, 2 * np.pi)
            px = int(center + spawn * np.cos(theta))
            py = int(center + spawn * np.sin(theta))
            continue

        # does it stick
        if sticking(px, py, grid, stickiness):
            grid[px, py] = i + 1
            stuck = True

            dist = np.sqrt((px - center)**2 + (py - center)**2)
            if dist > r_max:
                r_max = dist
                spawn = r_max + 1  # spawn just outside the current tree
                delete = r_max + 3

# plot
plt.imshow(grid, cmap='Grays')
plt.title(f"DLA Fractal (Stickiness: {stickiness})")
plt.axis('off')
plt.show()


# ###
# Extension 2: 2D Triangular Lattice

def move_2Dt(px, py):
    # aimless wandering
    direction = ra.randint(0, 5)
    if direction == 0: 
      px += 1
    elif direction == 1: 
      px -= 1
    elif direction == 2: 
      py += 1
    elif direction == 3: 
      py -= 1
    elif direction == 4: # Diagonal 1
      py += 1
      px += (1 if py % 2 == 1 else -1)
    elif direction == 5: # Diagonal 2
      py -= 1
      px += (1 if py % 2 == 1 else -1)
      
    return px, py




# ###
# Extension 3: 3D Lattice

def move_3d(px, py, pz):
  # aimless wandering
  direction = ra.randint(0, 5)
  if direction == 0: 
    px += 1
  elif direction == 1: 
    px -= 1
  elif direction == 2: 
    py += 1
  elif direction == 3:
    py -= 1
  elif direction == 4: 
    pz += 1
  elif direction == 5: 
    pz -= 1
    
  return px, py, pz















# ###
