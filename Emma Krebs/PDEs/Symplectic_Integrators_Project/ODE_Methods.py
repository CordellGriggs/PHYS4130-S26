'''
    Project name: Symplectic Integrations
    Subfolder: ODE Methods
    Author: Emma Krebs
    Final due date: 2/26/26
    File description: This file is to be used in the main.py. It includes the main three ODE's needed for 
                    comparison of the harmonic oscillator. This inlcudes a symplectic integration, RK45, 
                    and Odeint solvers.
'''


import numpy as np
import math
from scipy.integrate import odeint, solve_ivp


def Harmonic_oscillator(x_0, p_0, tmax, w, damp, N):
    
    t_array = np.linspace(0, tmax, N)
    x_array = []
    p_array = []

    for t in t_array:
        x = x_0 * math.cos(w*t) + p_0 * math.sin(w*t) / w
        p = p_0 * math.cos(w*t) - w*x_0*math.sin(w*t)
        x_array.append(x)
        p_array.append(p)
    
    return x_array, p_array, t_array


def Relative_error(analytic, estimated):
    return np.abs(analytic-estimated) / analytic


def Harmonic_deriv(t, y, w, damp):
    
    """
    Hammonic deriviation function for the other ODEs to use. Incorporates variables x and p
    as free values and returns how they change at that point in time.

    Args:
        t (int/float): Time (not used in this definition but passed to use in future ODEs).
        y (tuple): Starting position. Starting momentum.
        w (int/float): Angular frequency of harmonic oscillator.
        damp (int/float): Damping term on oscillator (if there is one)

    Returns:
        tuple: Functions for how dxdt and dpdt change in time.
    """
    x, p = y # Unpack our starting terms

    dxdt = p
    dpdt = -(w**2)*x - damp*p

    return [dxdt, dpdt]


def Verlet_symplectic(x_0, p_0, tmax, w, damp, N):

    """
    Modification of the Euler method for solving Hamiltonains. Yields better results than Euler
    by similarily using time steps but essentially flipped the order of the velocity update
    and the position update, computing the new velocity of the particle before we compute it's new position.
    In this function we use a symplectic euler method such that we calculate the new momentum before 
    the new position.

    Args:
        x_0 (int/float): Starting position.
        p_0 (int/float): Starting momentum.
        tmax (int/float): Max time range.
        w (int/float): Angular frequency for harmonic oscillator.
        damp (int/float): Dampening term on system.
        N (int): Number of steps for linspace (spacing).

    Returns:
        Three arrays: x_array and p_array of harmonic oscillator for a certain time/steps. Also include t_array from steps.
    """

    t_array = np.linspace(0, tmax, N)
    x_array = np.zeros(len(t_array))
    p_array = np.zeros(len(t_array))
    h = t_array[1] - t_array[0]
    x_array[0] = x_0
    p_array[0] = p_0

    # Get the next value
    a_0 = -w**2*x_0 - damp*p_0
    x_array[1] = x_0 + p_0*h + 0.5*a_0*h**2

    # Iterations, update momentum first then position
    for i in range(1, len(t_array) - 1):

        a = -w**2*x_array[i] - damp*((x_array[i] - x_array[i - 1])) / h # Acceleration
        x_array[i+1] = 2*x_array[i] - x_array[i - 1] + a*h**2

        p_array[i] = (x_array[i+1] - x_array[i - 1]) / (2*h)
    
    p_array[-1] = (x_array[-1] - x_array[-2]) / h

    return x_array, p_array, t_array


def RK45_solver(x_0, p_0, tmax, w, damp, N):

    """
    Calls the RK45 solver from scipy.integrate which is the Runge–Kutta–Fehlberg method, an 
    algorithm numerical analysis for the numerical solution of ODE's. 

    Args:
        x_0 (int/float): Starting position.
        p_0 (int/float): Starting momentum.
        tmax (int/float): Max time range.
        w (int/float): Angular frequency for harmonic oscillator.
        damp (int/float): Dampening term on system.
        N (int): Number of steps for linspace (spacing).
        
    Returns:
        Three arrays: Arrays for x values and p values for time. t_array for time is returned as well. 
    """

    y_0 = [x_0, p_0]
    t_array = np.linspace(0, tmax, N)
    # Force it to match other integration methods
    sol = solve_ivp(Harmonic_deriv, (0, tmax), y_0, method='RK45', t_eval=t_array, args=(w, damp)) 
    t_array = sol.t
    x_array = sol.y[0]
    p_array = sol.y[1]

    return x_array, p_array, t_array


def Odeint_solver(x_0, p_0, tmax, w, damp, N):

    """
    Calls the odeint function from scipy.integrate. odeint solves a system of ordinary 
    differential equations using lsoda from the FORTRAN library odepack.

    Args:
        x_0 (int/float): Starting position.
        p_0 (int/float): Starting momentum.
        tmax (int/float): Max time range.
        w (int/float): Angular frequency for harmonic oscillator.
        damp (int/float): Dampening term on system.
        N (int): Number of steps for linspace (spacing).

    Returns:
        tuple: Returns t as the t_array and N as an tuple of arrays, which incorporates 
        all the x and p values. 
    """
    y_0 = [x_0, p_0]

    t = np.linspace(0, tmax, N)
    L = odeint(Harmonic_deriv, y_0, t, args=(w, damp), tfirst=True, rtol=1e-4)
    
    return L[:,0], L[:,1], t


def Find_key(dict, value):
    """
    Grabs the key for a given value. This is used for labeling of graphs.

    Args: 
        dict (dictionary): Dictionary for the inputs to our solvers.
        value (array of int/floats): The key's value we are searching for.
    
    Returns:
        string: Returns either the key, or if there is no key, None. 
    
    """

    for key, val in dict.items():
        if val == value:
            return key
        
    return None


def Total_energy(x_array, p_array, w):

    """
    This function definition returns the kinetic, potential, and total energy for a given 
    array of x and p (along with their angular frequency) for a harmonic oscillator.

    Args:
        x_array (array): Array of x positions
        p_array (array): Array of p momentums
        w (int.float): Angular frequency

    Returns:
        Three arrays: Kinetic, potential, and total energy arrays
        
    """

    kinetic_energy = []
    potential_energy = []
    total_energy = []
    
    # Assuming m = 1, we can find the kinetic, potential, and total energy through the following methods
    for x, p in zip(x_array, p_array):
        KE_value = (1/2) * p**2
        PE_value = (1/2) * w**2 * x**2 # Since w is angular frequency and m = 1, so k = w**2
        TE_value = KE_value + PE_value

        kinetic_energy.append(KE_value)
        potential_energy.append(PE_value)
        total_energy.append(TE_value)
    
    return kinetic_energy, potential_energy, total_energy

