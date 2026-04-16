import Boring_Diffusion_Functions
import numpy as np
import matplotlib.pyplot as plt

grid_size = [500, 500]
num_particles = 10000
current_maximum = 1
generation_distance = 25
center = [grid_size[0]/2, grid_size[1]/2]
probability = 1
kill_distance = 100
stuck_locations = []

# Create our quick array. This will be holding the information of particles nearby
grid_array = np.zeros((grid_size[0], grid_size[1]), dtype=('i', 'i'))
count = 0

# Set initial seed 
grid_array[grid_size[0]//2][grid_size[1]//2] = 1

while count < num_particles:

    location = Boring_Diffusion_Functions.generation_sphere(current_maximum, generation_distance, center)
    particle = Boring_Diffusion_Functions.Particle(location, probability)

    while particle.stuck == False:

        particle.random_walk()
        if Boring_Diffusion_Functions.particle_from_center(particle, center) > kill_distance:
            print("KILLED")
            break  # kill particle

        neighbors = Boring_Diffusion_Functions.get_neighbors(particle.location)
        neighbor_count = 0
        touching = False

        for point in neighbors:
            # Check if anything is touching 
            if grid_array[point[0]][point[1]] == 1:
                touching = True
                neighbor_count += 1

        if touching and neighbor_count == 1: # Avoid overfilling and focus on tip growth by saying neighbor count = 1
            result = particle.sticky()
            if result == True:
                stuck_locations.append(particle.location)
                grid_array[particle.location[0]][particle.location[1]] = 1
                particle.stuck = True
                if Boring_Diffusion_Functions.particle_from_center(particle, center) > current_maximum:
                    current_maximum = Boring_Diffusion_Functions.particle_from_center(particle, center)
                    kill_distance = current_maximum + 50
                count += 1
            else: 
                continue

print(stuck_locations)
data = np.array(stuck_locations)
x, y = data.T
plt.scatter(x, y, marker='s', s=20)
plt.gca().set_facecolor('black')
plt.axis('equal')
plt.xlim(0, grid_size[0])
plt.ylim(0, grid_size[1])
plt.xticks(np.arange(0, grid_size[0]+1, 1))
plt.yticks(np.arange(0, grid_size[1]+1, 1))
plt.show()
