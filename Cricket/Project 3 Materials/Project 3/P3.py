'''
Filename: P3
Written by: Cricket Bergner
Date: 03/30/26
Purpose: Implement Project 3 and its extensions
'''
################################################################################

# import libraries
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint, solve_ivp
from scipy.spatial import ConvexHull
from P3_header import *

print('''
################################################################################
# Phase Space of a SHO
################################################################################
''')

# define initial variables
m = 1
k = 3
b = 0 # undamped
omega = np.sqrt(k/m)
damping = 0
nts = 1024 # larger nts, better approximation

N_initial = [1, 0]
tmin = 0
tmax = 10

# call the integrators
t_s, x_s, v_s = scipy_method(N_initial, tmin, tmax, nts, lambda N, t_odeint: deriv_odeint(N, t_odeint, omega, damping))
t_r, x_r, v_r = RK45_method(N_initial, tmin, tmax, nts, lambda t_ivp, N_ivp: deriv_ivp(t_ivp, N_ivp, omega, damping))
t_v, x_v, v_v = verlet(N_initial, tmin, tmax, nts, lambda x, v: accel(x, v, omega, damping))

# make the plots
plt.plot(v_r, x_r, color = '#f37fb0', label = "RK4", linewidth = 10)
plt.plot(v_v, x_v, 'o', color = '#61dbb0', label = "Verlet")
plt.plot(v_s, x_s, color = '#6316b0', label = "Scipy")
plt.xlabel("Velocity (m/s)")
plt.ylabel("Position (m)")
plt.title("Phase Space of a Harmonic Oscillator")
plt.legend()
plt.show()
print("")

# error plots
print("The error of the RK45and Scipy method as compared to the Velocity-Verlet value is shown below.")
print("")

# compute errors relative to Verlet
error_x_r = (x_r[:nts] - x_v[:nts]) 
error_v_r = (v_r[:nts] - v_v[:nts]) 

error_x_v = (x_v[:nts] - x_v[:nts])
error_v_v = (v_v[:nts] - v_v[:nts]) 

error_x_s = (x_s[:nts] - x_v[:nts]) 
error_v_s = (v_s[:nts] - v_v[:nts]) 

error_r = np.sqrt(error_x_r**2 + error_v_r**2)
error_s = np.sqrt(error_x_s**2 + error_v_s**2)
error_v = np.sqrt(error_x_v**2 + error_v_v**2)

# plot the errors
plt.plot(t_v[:nts], error_r[:nts], label="RK45 Error", color='#f37fb0')
plt.plot(t_v[:nts], error_s[:nts], label="Scipy Error", color='#6316b0')
plt.plot(t_v[:nts], error_v[:nts], '--', label="Verlet (baseline)", color='#61dbb0')
plt.xlabel("Time (s)")
plt.ylabel("Phase Space Error")
plt.title("Total Error vs Time")
plt.legend()
plt.show()
print("")

plt.plot(t_v[:nts], error_r[:nts], label="RK45 Error", color='#f37fb0')
plt.plot(t_v[:nts], error_s[:nts], label="Scipy Error", color='#6316b0')
plt.plot(t_v[:nts], error_v[:nts], '--', label="Verlet (baseline)", color='#61dbb0')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Time (s)")
plt.ylabel("Phase Space Error")
plt.title("Total Error vs Time (Log-Log)")
plt.legend()
plt.show()
print("")

print('''
################################################################################
# Phase Space of a SHO with a Damping Term
################################################################################
''')

# damping term added
damping = 0.2 / m

N_initial = [1, 0]
tmin = 0
tmax = 100

# call the integrators
nt_s, nx_s, nv_s = scipy_method(N_initial, tmin, tmax, nts, lambda N, t_odeint: deriv_odeint(N, t_odeint, omega, damping))
nt_r, nx_r, nv_r = RK45_method(N_initial, tmin, tmax, nts, lambda t_ivp, N_ivp: deriv_ivp(t_ivp, N_ivp, omega, damping))
nt_v, nx_v, nv_v = verlet(N_initial, tmin, tmax, nts, lambda x, v: accel(x, v, omega, damping))

# make the plots
plt.plot(nv_r, nx_r, 'o', color = '#f37fb0', label = "RK4", linewidth = 20)
plt.plot(nv_v, nx_v, color = '#61dbb0', label = "Verlet")
plt.plot(nv_s, nx_s, color = '#6316b0', label = "Scipy")
plt.xlabel("Velocity (m/s)")
plt.ylabel("Position (m)")
plt.title("Phase Space of a Harmonic Oscillator with Damping Term")
plt.legend()
plt.show()
print("")

# error plots
print("The error of the RK45 and Scipy method as compared to the Velocity-Verlet value for a damped SHO is shown below.")
print("")

# compute errors relative to Verlet
error_x_r_d = (nx_r[:nts] - nx_v[:nts]) 
error_v_r_d = (nv_r[:nts] - nv_v[:nts]) 

error_x_v_d = (nx_v[:nts] - nx_v[:nts])
error_v_v_d = (nv_v[:nts] - nv_v[:nts]) 

error_x_s_d = (nx_s[:nts] - nx_v[:nts]) 
error_v_s_d = (nv_s[:nts] - nv_v[:nts]) 

error_r_d = np.sqrt(error_x_r_d**2 + error_v_r_d**2)
error_s_d = np.sqrt(error_x_s_d**2 + error_v_s_d**2)
error_v_d = np.sqrt(error_x_v_d**2 + error_v_v_d**2)

# plot the errors
plt.plot(nt_v[:nts], error_r_d[:nts], label="RK45 Error", color='#f37fb0')
plt.plot(nt_v[:nts], error_s_d[:nts], label="Scipy Error", color='#6316b0')
plt.plot(nt_v[:nts], error_v_d[:nts], '--', label="Verlet (baseline)", color='#61dbb0')
plt.xlabel("Time (s)")
plt.ylabel("Phase Space Error")
plt.title("Total Error vs Time")
plt.legend()
plt.show()
print("")

plt.plot(nt_v[:nts], error_r_d[:nts], label="RK45 Error", color='#f37fb0')
plt.plot(nt_v[:nts], error_s_d[:nts], label="Scipy Error", color='#6316b0')
plt.plot(nt_v[:nts], error_v_d[:nts], '--', label="Verlet (baseline)", color='#61dbb0')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Time (s)")
plt.ylabel("Phase Space Error")
plt.title("Total Error vs Time (Log-Log)")
plt.legend()
plt.show()
print("")

print('''
################################################################################
# Total Mechanical Energy
################################################################################
''')

# total mechanical energy
E_r = 0.5*m*v_r**2 + 0.5*k*x_r**2
E_v = 0.5*m*v_v**2 + 0.5*k*x_v**2
E_s = 0.5*m*v_s**2 + 0.5*k*x_s**2

# make the plots
plt.plot(t_r, E_r, color = '#f37fb0', label = "RK4")
plt.plot(t_v[:nts], E_v[:nts], color = '#61dbb0', label = "Verlet")
plt.plot(t_s, E_s, color = '#6316b0', label = "Scipy")
plt.xlabel("Time (s)")
plt.ylabel("Energy (J)")
plt.title("Total Mechanical Energy Over Time")
plt.legend()
plt.show()
print("")

# plot the errors
print("The error of the RK45 and Scipy method as compared to the Velocity-Verlet value is shown below.")
print("")

error_r = E_r[:nts] - E_v[:nts]
error_s = E_s[:nts] - E_v[:nts]
error_v = E_v[:nts] - E_v[:nts]

plt.plot(t_v[:nts], error_r[:nts], label="RK45 Error", color='#f37fb0')
plt.plot(t_v[:nts], error_s[:nts], label="Scipy Error", color='#6316b0')
plt.plot(t_v[:nts], error_v[:nts], '--', label="Verlet (Baseline)", color='#61dbb0')
plt.xlabel("Time (s)")
plt.ylabel("Energy Difference (J)")
plt.title("Energy Error")
plt.legend()
plt.show()
print("")

plt.plot(t_v[:nts], error_r[:nts], label="RK45 Error", color='#f37fb0')
plt.plot(t_v[:nts], error_s[:nts], label="Scipy Error", color='#6316b0')
plt.plot(t_v[:nts], error_v[:nts], '--', label="Verlet (Baseline)", color='#61dbb0')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Time (s)")
plt.ylabel("Energy Difference (J)")
plt.title("Energy Error (Log-Log)")
plt.legend()
plt.show()
print("")

# damped case
nE_r = 0.5*m*nv_r**2 + 0.5*k*nx_r**2
nE_v = 0.5*m*nv_v**2 + 0.5*k*nx_v**2
nE_s = 0.5*m*nv_s**2 + 0.5*k*nx_s**2

plt.plot(nt_r, nE_r, 'o', color = '#f37fb0', label = "RK4")
plt.plot(nt_v, nE_v, color = '#61dbb0', label = "Verlet")
plt.plot(nt_s, nE_s, color = '#6316b0', label = "Scipy")
plt.xlabel("Time (s)")
plt.ylabel("Energy (J)")
plt.title("Total Mechanical Energy Over Time (Damped)")
plt.legend()
plt.show()
print("")

# damped error
print("The error of the RK45 and Scipy method as compared to the Velocity-Verlet value for a damped SHO is shown below.")
print("")

error_r_d = nE_r[:nts] - nE_v[:nts]
error_s_d = nE_s[:nts] - nE_v[:nts]
error_v_d = nE_v[:nts] - nE_v[:nts]

plt.plot(nt_v[:nts], error_r_d[:nts], label="RK45 Error", color='#f37fb0')
plt.plot(nt_v[:nts], error_s_d[:nts], label="Scipy Error", color='#6316b0')
plt.plot(nt_v[:nts], error_v_d[:nts], '--', label="Verlet (Baseline)", color='#61dbb0')
plt.xlabel("Time (s)")
plt.ylabel("Energy Difference (J)")
plt.title("Energy Error (Damped)")
plt.legend()
plt.show()
print("")

plt.plot(nt_v[:nts], error_r_d[:nts], label="RK45 Error", color='#f37fb0')
plt.plot(nt_v[:nts], error_s_d[:nts], label="Scipy Error", color='#6316b0')
plt.plot(nt_v[:nts], error_v_d[:nts], '--', label="Verlet (Baseline)", color='#61dbb0')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Time (s)")
plt.ylabel("Energy Difference (J)")
plt.title("Damped Energy Error (Log-Log)")
plt.legend()
plt.show()
print("")

#################################################################################################
print('''
################################################################################
# Extension 1 - Phase Space Area
################################################################################
''')

# set initial variables
delta = 0.1
damped = 0.2
mesh = [4, 32] # first evolving over 4 points, then 32

for Ngrid in mesh:

  x_pts = np.linspace(1 - delta, 1 + delta, Ngrid)
  v_pts = np.linspace(0 - delta, 0 + delta, Ngrid)
  pts = [(x, v) for x in x_pts for v in v_pts]

  t, straj, rtraj, vtraj, straj_d, rtraj_d, vtraj_d = three_solvers(pts, omega, damping)

  area_s = psa(straj)
  area_r = psa(rtraj)
  area_v = psa(vtraj)

  area_s_d = psa(straj_d)
  area_r_d = psa(rtraj_d)
  area_v_d = psa(vtraj_d)

  # plots
  print("")
  print("Plots for grid", Ngrid, "by", Ngrid)
  print("")
  plt.plot(t, area_s, color = 'red', label="Scipy")
  plt.plot(t, area_r, color = 'goldenrod', label="RK45")
  plt.plot(t, area_v[:len(t)], '--', color = 'blue', label="Verlet")
  plt.xlabel("Time (s)")
  plt.ylabel("Phase Space Area (m^2)")
  plt.title("Undamped Osciallator")
  plt.legend()
  plt.show()
  print("")

  # error plots

  error_s = area_s[:len(t)] - area_v[:len(t)]
  error_r = area_r[:len(t)] - area_v[:len(t)]
  error_v = area_v[:len(t)] - area_v[:len(t)]

  plt.plot(t, error_s, label="Scipy Error", color='red')
  plt.plot(t, error_r, label="RK45 Error", color='goldenrod')
  plt.plot(t, error_v[:len(t)], '--', label="Verlet (baseline)", color='blue')
  plt.xscale('log')
  plt.yscale('log')
  plt.xlabel("Time (s)")
  plt.ylabel("Area Error (m^2)")
  plt.title(f"Phase Space Area Error (Undamped, {Ngrid}x{Ngrid}, Log-Log)")
  plt.legend()
  plt.show()
  print("")

  # damped case plots

  plt.plot(t, area_s_d, 'o', color = 'red', label="Scipy")
  plt.plot(t, area_r_d, color = 'green', label="RK45")
  plt.plot(t, area_v_d[:len(t)], '--', color = 'blue', label="Verlet")
  plt.xlabel("Time (s)")
  plt.ylabel("Phase Space Area (m^2)")
  plt.title("Damped Oscillator")
  plt.legend()
  plt.show()
  print("")

  # damped error

  error_s_d = area_s_d[:len(t)] - area_v_d[:len(t)]
  error_r_d = area_r_d[:len(t)] - area_v_d[:len(t)]
  error_v_d = area_v_d[:len(t)] - area_v_d[:len(t)]

  plt.plot(t, error_s_d, label="Scipy Error", color='red')
  plt.plot(t, error_r_d, label="RK45 Error", color='green')
  plt.plot(t, error_v_d[:len(t)], '--', label="Verlet (baseline)", color='blue')
  plt.xscale('log')
  plt.yscale('log')
  plt.xlabel("Time (s)")
  plt.ylabel("Area Error (m^2)")
  plt.title(f"Phase Space Area Error (Damped, {Ngrid}x{Ngrid}, Log-Log)")
  plt.legend()
  plt.show()


print('''################################################################################
# Extension 2
################################################################################
''')

print("For an undamped SHO, the area should remain unchanged. We can test this by taking the determinant of the matrix.")
print("")

qn, pn = 1.0, 2.0
dt = 0.2

j = jacobian(lambda q, p, dt: onestep_verlet(q, p, dt, omega, damping), qn, pn, dt)
det = np.linalg.det(j)

j_rk = jacobian(lambda q, p, dt: onestep_rk45(q, p, dt, omega, damping), qn, pn, dt)
det_rk = np.linalg.det(j_rk)

j_s = jacobian(lambda q, p, dt: onestep_odeint(q, p, dt, omega, damping), qn, pn, dt)
det_s = np.linalg.det(j_s)

print("Velocity-Verlet:")
print(f"Determinant: {det:.1f}")
print("")
print("RK45:")
print(f"Determinant: {det_rk:.3f}")
print("")
print("Scipy odeint:")
print(f"Determinant: {det_s:.3f}")
print("")

print("The determinant is one for the Verlet integrator.")
print("Thus, for the higher order integrator, phase space area is conserved.")

################################################################################