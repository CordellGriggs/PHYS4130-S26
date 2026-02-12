'''
    Project name: Numeric Integration Startup
    Author: Emma Krebs
    Final due date: 2/17/26
    Project description: This project has the student use their knowledge of numerical integration methods
'''

import numpy
import pandas as pd
import math

# ------------------ Function Definitions ------------------

'''
    Definition: trapezoid_function
    Parameters: func (Given function), a (Starting point of subdivision), b (Ending point of subdivision),
        and n (the number of subintevrals).
    Description: Takes in a function, a starting point, and an ending point and goes through an increasing
        number of subintervals to come to the closest *********
'''
def trapezoid_function(func, a, b, n):

    h = (b - a) / n # Width of our subinterval
    sum = 0
    # Loop for number of subintervals
    for i in range(n):
        sum += (1 / 2) * h * (func(a + i * h) + func(a + i * h + h))

    return sum


'''
    Definition: error_calc
    Parameters: current (Current sum) and true (true value)
    Description: Calculates the error percentage between the given sum and the true value of integral.
'''
def error_calc(current, true):
    return round((abs(current - true) / true) * 100, 5)


'''
    Definition: approximator
    Parameters: f (Given function), start (Starting point of subdivision), end (Ending point of subdivision),
        true_value (Correct value of integral that we will use for approximation), and value of sig_fig we
        are interested in.
    Description: **********
'''
def approximator(f, start, end, true_value, sig_fig):

    n = 1 # Starting number of subintervals
    sums = [] # Empty array to keep track of the sum of the function using n integrals
    parameter = False # Parameter used to know when to end loop once we have approximated close to the answer

    while(parameter == False):

        current_sum = trapezoid_function(f, start, end, n)
        error = error_calc(current_sum, true_value)
        sums.append((n, current_sum, str(error) + '%'))
        
        if error <= sig_fig:
            parameter = True
        else:
            n *= 2

    return sums


'''
    Definition: given_function
    Parameters: x (When called it will plug in the x value)
    Description: Simplifies writing out the function when passed to the trapezoid function
'''
def given_function(x):
    return math.sin(math.sqrt(100*x)) ** 2


# ------------------ Main Body ------------------

# For trapezoid section
results = approximator(given_function, 0, 2, 1.00570254283, 0.00005)
# Create table
pd.set_option('display.precision', 10)
df = pd.DataFrame(results, columns=['Number of intervals', 'Summation of Integral', 'Error from true answer(%)'])
print(df)

# For Gaussian 