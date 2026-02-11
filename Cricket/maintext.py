#########################################################################
#Author: Cricket Bergner
#Date: 02/10/2026
#########################################################################
print("#########################################################################")
print("")
print("")
print("Adaptive Integration")
print("")
print("")
#########################################################################
print("#########################################################################")

# import libraries
import numpy as np
import math as m
from prettytable import PrettyTable as pt

# initialize variables
counter = itl = e = 0
N = 1
ans = 1.005702542825726 #from https://www.integral-calculator.com
t = pt(["Number of Slices", "Integral Estimate", "Estimate of Error"])

# trapezoid rule
def trap(f, a, b, N):
  dx = (b-a)/N
  s = 0 # sum  
  for i in range(N):
    xi = a + (i*dx)
    xip = a + ((i+1)*dx)
    s += ((f(xi) + f(xip))* (dx / 2))
  return s

# while loop to iterate until conditions of problem are met
while counter < 13:
  N *= 2
  counter += 1
  itl = trap(lambda x: np.sin(np.sqrt(100*x))**2, 0, 2, N) # calculate integral
  e =  np.abs(itl - ans) # calculate error
  t.add_row([N, round(itl, 7), round(e, 7)]) # add to table
  
print(t) # table
print("The correct output to the integral is ", ans, ".")
print("It took 8192 intervals for the trapezoid rule to approximate this with an accuracy of 10^-6.")

#########################################################################
print("#########################################################################")
print("")
print("")
print("Gaussian Quadrature")
print("")
print("")

#map the integral from [0,2] to [-1,1] using the u-substitution given
# use the scipy function to get sample pts and weights
# implement the gaussian quadrature formula
# test it on the integral
# verfiy that the u function works
# calculate du

#########################################################################
print("#########################################################################")





#########################################################################
print("#########################################################################")
print("")
print("")
print("Subplots")
print("")
print("")
print("#########################################################################")

# import libraries
import scipy as sp
import matplotlib.pyplot as plt
from scipy.special import legendre as l

# initialize variables
x = np.linspace(-1, 1, 400)

# create figure with subplots
f, a = plt.subplots(4, 4, figsize=(16, 16))
f.suptitle('Legendre Polynomials', fontsize=16)

for i in range(4):  # rows
    for j in range(4):  # columns
        ax = a[i, j]
        
        # load Legendre polynomials and their evaluations at x
        # source: https://python4physics.in/program/python/program.php?menu_id=14&submenu_id=2#gsc.tab=0
        Pi = l(i+1)
        Pj = l(j+1)
        Piv = Pi(x) 
        Pjv = Pj(x)
      
        # make the plots
        ax.plot(x, Piv, label=f'P_{i+1}(x)', color='goldenrod', linewidth=1.75)
        ax.plot(x, Pjv, label=f'P_{j+1}(x)', color='purple', linewidth=1.5)
        ax.plot(x, Piv*Pjv, label='Product', color='#78C3F5', linewidth=2)
        
        #label everything for coherency
        ax.set_xlabel('x', fontsize=8)
        ax.set_ylabel('P_n(x)', fontsize=8)
        ax.set_title(f'P_{i+1}, P_{j+1}, P_{i+1}·P_{j+1}', fontsize=10)
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=7)

plt.tight_layout()
plt.show()

#########################################################################
print("#########################################################################")
