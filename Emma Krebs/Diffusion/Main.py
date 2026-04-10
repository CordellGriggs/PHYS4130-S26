import Diffusion


# ------- Starting Parameters -------
n = 3 # Number of iterations of our octree. Depends on our grid space.
num_particles = 100 # Number of particles used in simulation

grid_value = 8**n
grid = [grid_value, grid_value, grid_value]
center = [grid_value/2, grid_value/2, grid_value/2]
probability = 1 # probability of something sticking when encountering a particle
stuck_particles = [] # The number of stuck particles that appear. Once in order, we can generate them.
current_maximum = 1 # Will be updated as our program exapnds. 
generation_distance = 5 # The distance to the surface of a sphere for generating a new particle

# Generate the very first seed and root

root = Diffusion.Node(center, grid, 1)
seed_particle = Diffusion.Particle(center, probability)
Diffusion.insert_particle(root, seed_particle, n)

for num in range(num_particles):
    location = Diffusion.generation_sphere(current_maximum, generation_distance, center)
    particle = Diffusion.Particle(location, probability)
    print(f"Location: {location}")

    print(f'Iteration {num}')

    Diffusion.insert_particle(root, particle, n)
    for i in range(8):
        print(root.children[i].particles)
