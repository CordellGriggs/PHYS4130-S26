import numpy as np
import matplotlib.pyplot as plt


def Symplectic_Euler(start_v, start_u, w, h, steps):

    v_array = []
    u_array = []

    v_array.append(start_v)
    u_array.append(start_u)

    prev_v = start_v
    prev_u = start_u

    for i in range(steps):

        curr_v = prev_v + h*prev_u
        curr_u = prev_u - h*(w**2)*curr_v

        v_array.append(curr_v)
        u_array.append(curr_u)

        prev_v = curr_v
        prev_u = curr_u
    
    return v_array, u_array

x_array, p_array = Symplectic_Euler(1, 1, 1, 0.025, 10)

plt.plot(x_array, p_array)
plt.plot()

