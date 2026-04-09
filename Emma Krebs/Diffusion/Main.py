import Diffusion


# ------- Starting Parameters -------
n = 3 # Number of iterations of our octree. Depends on our grid space.
num_particles = 100 # Number of particles used in simulation

grid_value = 8**n
grid = [grid_value, grid_value, grid_value]
center = [grid_value/2, grid_value/2, grid_value/2]
probability = 1 # probability of something sticking when encountering a particle
stuck_particles = [] # The number of stuck particles that appear. Once in order, we can generate them.

# Generate the very first seed and root



