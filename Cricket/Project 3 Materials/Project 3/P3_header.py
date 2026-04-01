'''
Filename: P3_header
Written by: Cricket Bergner
Date: 03/30/26
Purpose: "header" file to gather all the functions
'''

# import libraries
import numpy as np
from scipy.spatial import ConvexHull
from scipy.integrate import odeint, solve_ivp

# derivative function for the velocity-verlet symplectic integrator
def accel(x, v, omega, damping):
    return -omega**2*x - damping*v

# derivative function for the RK45 symplectic integrator
def deriv_ivp(t, N, omega, damping):
    x, v = N
    dxdt = v
    dvdt = -omega**2*x - damping*v
    return [dxdt, dvdt]

# derivative function for the scipy integrator
def deriv_odeint(N, t, omega, damping):
    x, v = N
    dxdt = v
    dvdt = -omega**2*x - damping*v
    return [dxdt, dvdt]

# calculates jacobian for the matrix
def jacobian(int_func, qn, pn, dt, epsilon=1e-6):
  q_next, p_next = int_func(qn, pn, dt) # get result for the timestep

  qq_next, pq_next = int_func(qn + epsilon, pn, dt) # get result for the nudged q
  dq = (np.array([qq_next, pq_next]) - np.array([q_next, p_next])) / epsilon # derivative of q

  qp_next, pp_next = int_func(qn, pn + epsilon, dt) # get result for the nudged p
  dp = (np.array([qp_next, pp_next]) - np.array([q_next, p_next])) / epsilon # derivative of p

  jacobian = np.column_stack((dq, dp)) # assemble the matrix

  return jacobian

# scipy integrator function but for only one time step
def onestep_odeint(q, p, dt, omega, damping):
  def deriv(N, t):
    x, v = N
    dxdt = v
    dvdt = -omega**2 * x - damping * v
    return [dxdt, dvdt]
     
  t_span = [0, dt]
  sol = odeint(deriv, [q, p], t_span)
  nq = sol[-1, 0]
  np = sol[-1, 1]

  return nq, np

# RK45 function but for only one time step
def onestep_rk45(q, p, dt, omega, damping):
    # simple Euler-like step using derivatives (approximate)
    dqdt = p
    dpdt = -omega**2 * q - damping * p
    nq = q + dt * dqdt
    np = p + dt * dpdt
    return nq, np

# velocity-verlet function but only for one time step
def onestep_verlet(q, p, dt, omega, damping):
    a = -omega**2 * q - damping * p
    p_half = p + 0.5 * dt * a
    nq = q + dt * p_half
    na = -omega**2 * nq - damping * p_half
    np = p_half + 0.5 * dt * na

    return nq, np

# calculates phase space area
def psa(traj_list): # psa = phase space area
  nts = len(traj_list[0][0]) # length of the 2D array
  area = np.zeros(nts) # fill it with zeroes

  for i in range(nts): # loop through each time step
    pts = np.array([[t[0][i], t[1][i]] for t in traj_list]) # stack (x, v) for each particle
    hull = ConvexHull(pts) #calculates area
    area[i] = hull.volume # it says volume but really it is returning an area

  return area

# RK4(5) scipy function
def RK45_method(N_initial, tmin, tmax, nts, deriv):
  t = np.linspace(tmin, tmax, nts)
  sol = solve_ivp(deriv, (tmin, tmax), N_initial, method='RK45', t_eval=t)
  x = sol.y[0]
  v = sol.y[1]

  return t, x, v

# Scipy Method
def scipy_method(N_initial, tmin, tmax, nts, deriv):
    t = np.linspace(tmin, tmax, nts)
    N = odeint(deriv, N_initial, t)
    x = N[:,0]
    v = N[:,1]

    return t, x, v

# function that runs all three symplectic integrators for damped and undamped oscillators
def three_solvers(pts, omega, damping): 
  straj, rtraj, vtraj = [], [], [] # short for scipy trajectories (undamped)
  straj_d, rtraj_d, vtraj_d = [], [], [] # damped

  for (x0,v0) in pts: # for every point in the 2D array
    st, sx, sv = scipy_method([x0, v0], tmin, tmax, nts, lambda N, t: deriv_odeint(N, t, omega, 0))
    straj.append((sx, sv))

    _, rx, rv = RK45_method([x0, v0], tmin, tmax, nts, lambda t, N: deriv_ivp(t, N, omega, 0))
    rtraj.append((rx, rv))

    _, vx, vv = verlet([x0, v0], tmin, tmax, nts, lambda x, v: accel(x, v, omega, 0))
    vtraj.append((vx, vv))

    _, sx_d, sv_d = scipy_method([x0, v0], tmin, tmax, nts, lambda N, t: deriv_odeint(N, t, omega, damped))
    straj_d.append((sx_d, sv_d))

    _, rx_d, rv_d = RK45_method([x0, v0], tmin, tmax, nts, lambda t, N: deriv_ivp(t, N, omega, damped))
    rtraj_d.append((rx_d, rv_d))

    _, vx_d, vv_d = verlet([x0, v0], tmin, tmax, nts, lambda x, v: accel(x, v, omega, damped))
    vtraj_d.append((vx_d, vv_d))

  return st, straj, rtraj, vtraj, straj_d, rtraj_d, vtraj_d

# velocity-verlet symplectic integrator 
def verlet(N_initial, tmin, tmax, nts, deriv):

  # define inital variables
  x0, v0 = N_initial
  x = np.zeros(nts + 1)
  v = np.zeros(nts + 1)
  x[0] = x0
  v[0] = v0
  t = np.linspace(tmin, tmax, nts + 1)
  dt = t[1] - t[0]

  # loop
  for i in range(nts):
    a = deriv(x[i], v[i])
    v_half = v[i] + 0.5 * dt * a
    x[i+1] = x[i] + dt * v_half
    a_new = deriv(x[i+1], v_half)
    v[i+1] = v_half + 0.5 * dt * a_new

  return t, x, v

#################################################################################