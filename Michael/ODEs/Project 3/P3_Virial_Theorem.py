import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import uniform
from P3_Methods import Yoshida

# Simulation Parameters ----------------------------------------------------------------------
G = 5 #Gravitational Constant 

M =  [1, 1, 2]              # Masses
X0 = [[-1,0], [1,0], [2,2]] # Initial Positions
V0 = [[0,-1], [0,1], [1,0]] # Initial Velocities

tmin = 0
tmax = 5
nts = 100

# Funcitons to Compute Derivatives ----------------------------------------------------------------------
def GravAcc(P1, P2, M2): #acceleration on P1 from P2
    if np.array_equal(P1, P2): #Impportant edge case
        return np.array([0,0])
    else:
        return G*M2*(P2 - P1)/((np.linalg.norm(P2 - P1)**3)) #Gravitational acceleration formula
    
def TotalGrav(P, X, M): # Calculates acceleratio on P from all points in X
    A = np.array([0, 0])
    for i in range(len(X)):
        A = A + GravAcc(P, X[i], M[i])
    return A

def Derivative(t, U): # U is a 2 element list. The first element is the array of position. The second is velocities
    X, Y = U

    dX_dt = Y
    dY_dt = np.asarray([TotalGrav(X[i], X, M) for i in range(len(X))])
    return [dX_dt, dY_dt]

# Check That the Right Number of Conditions Have Been Given -----------------------------------------------------
if len(X0) != len(V0) or len(X0) != len(M):
    print()
    print("Inconsistent number of initial conditions or masses!")
    print("The following should all be equal:")
    print("Number of Point Masses:       ", len(M))
    print("Number of Initial Positions:  ", len(X0) )
    print("Number of Initial Velocities: ", len(V0))
    print()
    exit()

# Calculating and Plotting the Trajectories ------------------------------------------------------------------
    # Note: Strucutre of sol: 
    # sol = [times, [trajectory 1, velocity 1], [trajectory 2, velocity 2], ...]
    # where trajectories and velocities are two element np arrays.

sol = Yoshida(X0, V0, tmin, tmax, nts, Derivative) # All the parameters

for i in range(len(X0)):
    points = np.array(sol[i + 1][0])
    plt.plot(points[:, 0], points[:, 1]) #The : means to loop over all such elements

plt.show()

# Animatinge Attempt 3
t = sol[0]
trajectories = [P[0] for P in sol[1:] ]# = [traj1, traj2, traj3, ...]
print((trajectories[0][0]))
n = len(X0)

fig, ax = plt.subplots()

all_points = np.vstack(trajectories)
ax.set_xlim(all_points[:, 0].min(), all_points[:, 0].max())
ax.set_ylim(all_points[:, 1].min(), all_points[:, 1].max())

points = [ax.plot([], [], 'o')[0] for _ in range(n)]

def init():
    for p in points:
        p.set_data([], [])
    return points

def update(frame):
    for i, p in enumerate(points):
        x, y = trajectories[i][frame]
        p.set_data(x, y)
    return points

#ani = FuncAnimation(fig, update, frames = len(t), init_func = init, blit=True)

plt.show()