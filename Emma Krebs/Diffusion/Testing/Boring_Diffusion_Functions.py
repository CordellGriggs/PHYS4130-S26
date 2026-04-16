import numpy as np
import random


class Particle:
    '''
        Class: Particle
        Description: Particle object that stores location, age, and probability. Can call a random walk on itself
        and store the data.
    '''
    def __init__(self, location, probability):
        self.location = location
        self.probability = probability
        self.stuck = False

    def random_walk(self):
        dx, dy = random.choice([[-1, 0], [0, 1], [0, -1], [1, 0]])
        self.location[0] += dx
        self.location[1] += dy
        

    def sticky(self):
        # This particle has the potential to get stuck. Check all particles nearby. 

        prob = self.probability
        if random.uniform(0, 1) <= prob:
            print("Sticky")
            return True
            
        return False # It was not stuck
            


def get_neighbors(location):
    '''
        Grabs the surrounding neighbors. Includes diagonals as well for a total of eight neighbors.

        Args:
            location: Center location of where a particl is. 

        Return:
            neighborhood: A list of points around our given location for a 2D grid. 
    '''

    offsets = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    neighborhood = []

    for offset in offsets: # For x coordinate
        grid_x = location[0] + offset[0]
        grid_y = location[1] + offset[1]

        neighbor = [grid_x, grid_y]
        neighborhood.append(neighbor)

    return neighborhood


def generation_sphere(current_maximum, generation_distance, center):
    '''
        Generates a location for a new particle based on the current size of DLA and set generation distance
        by the user.

        Args:
            current_maximum (int): The current furthest distance of a particle from the sphere.
            generation_distance (int): Preset value by the user between current_maximum and shell generation
            center (array): Array of center coordintaes

        Returns:
            location (array): Location of where new particle has been spawned in.
    '''

    radius = current_maximum + generation_distance
    u = random.uniform(0,1)
    v = random.uniform(0,1)

    # From a source in document to create a sphere with equally likely random points on it
    theta = 2*np.pi*u
    px = int(np.cos(theta) * radius + center[0])
    py = int(np.sin(theta) * radius + center[1])

    location = [px, py]

    return location


def particle_from_center(particle, center):
    '''
        Measures particle from center.

        Arg:
            particle (object): Particle being measured
            center (array): Center of grid

        Returns: 
            distance (int): Distance from center
    '''
    location = particle.location

    distance = np.sqrt((location[0] - center[0])**2 + (location[1] - center[1])**2)
    return distance
