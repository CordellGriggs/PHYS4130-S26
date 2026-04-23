
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from P4_Functions import AddPoint, box_counting_dimension

# DLA Simulation =======================================================================================
#simul
# simulation parameters
L = 600   #number of slots on one edge of the array
N = 5000  #number of points to add to the aggregate
S = 1    #sticknynesss

#Create the aggregate
Aggregate = np.zeros((L,L)) 
center = (L-1)//2
Aggregate[center, center] = 10000 #seed point

fig, ax = plt.subplots()
im = ax.imshow(Aggregate, cmap='magma', vmin = 0, vmax = N)

#Computation parameters anf histogram
r_eff = 2 #inital effective radius
color_offset = N/4

thetaMin = -np.pi
thetaMax = np.pi
numBins = 30

bin_edges = np.linspace(thetaMin, thetaMax, 1+numBins)
angle_histo = np.zeros(numBins, dtype=int)

# Simulatiing
def update(frame):
    global r_eff
    r_eff = AddPoint(Aggregate, r_eff, S, L, angle_histo, bin_edges, frame+1, color_offset)
    im.set_array(Aggregate)

    coords = np.argwhere(Aggregate)

    ymin, xmin = coords.min(axis=0)
    ymax, xmax = coords.max(axis=0)
    lower = min([xmin, ymin])
    upper = max([xmax, ymax])

    ax.set_xlim(lower, upper)
    ax.set_ylim(lower, upper)

    if (frame + 1)%25 == 0:
        print(frame + 1, " of ", N, " points. Effective Radius: ", r_eff)

    return [im]

ani = FuncAnimation(fig, update, frames = N, interval = 10, blit=False, repeat = False) #repeat=False or else it adds points forever

#live animation
plt.show()

print(angle_histo)
plt.plot(bin_edges[0:len(bin_edges)-1], angle_histo)
D, sizes, counts = box_counting_dimension(Aggregate)

print(D)