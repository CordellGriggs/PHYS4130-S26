
import numpy as np
import scipy as sp
import matplotlib.pyplot as py

#Integrands------------------------------------------------------------------------------------------------------------
def f(x):#first integrand
    return (np.sin(np.sqrt(100*x)))**2

def g(x):#second integrand with a singularity at x = 2
    return (x**2)/np.sqrt(2-x)

def G(u): #transformed g(x) into u domain. It also has the prefactor from du
    return 8*np.sqrt(2)*(np.sin(u))**5

#Integration algorithms-------------------------------------------------------------------------------------------------
def trapezoid(f,a,b,N):
    h = (b-a)/N #Interval size
    mysum = 0
    
    for i in range(1,N): #should go from 1 to N-1
        mysum = mysum + float(f(a+(i)*h)*h) 
    return mysum +(h/2)*(f(a) + f(b))

def midpoint(f,a,b,N):
    h = (b-a)/N 
    mysum = 0
    
    for i in range(N):
        mysum = mysum + float(f(a+(i+0.5)*h)*h) 
    return mysum

def Homer(f,a,b,N): 
        return (1/3)*trapezoid(f,a,b,N) + (2/3)*midpoint(f,a,b,N)

def GaussQuad(g,a,b,N):
    roots, weights = sp.special.roots_legendre(N)
    return np.sum([weights[i]*g(((b-a)/2)*roots[i] + (a+b)/2)*(b-a)/2 for i in range(N)])


# Outputting functions---------------------------------------------------------------------------
def Table(g,a,b,TrueVal, alg,points): #Plots table of values from the trapezoid rule

    print('\n',f"{'Intervals':<12} {'Approx Value':>16} {'Error' :>25}")
    for i in points:
        val = alg(g,a,b,i)
        print(f"{i:10d} {val:19.10f} {np.abs(TrueVal - val):25.20f}")
    print()
    return

def PlotStuff(): #Plots the legendre polynomials
    x = np.linspace(-1,1,100)
    fig, ax = py.subplots(4,4)

    for i in range(4):
        for j in range(4):
            #This was based on Cricket's code
            # make the plots
            ax[i,j].plot(x, P(i+1,x), label=f'P_{i+1}(x)', color='goldenrod', linewidth=1.75)
            ax[i,j].plot(x, P(j+1,x), label=f'P_{j+1}(x)', color='purple', linewidth=1.5)
            ax[i,j].plot(x, P(i+1,x)*P(j+1,x), label='Product', color='#78C3F5', linewidth=2)
            
            #labela and stuff
            ax[i,j].set_xlabel('x', fontsize=8)
            ax[i,j].set_ylabel('P_n(x)', fontsize=8)
            ax[i,j].set_title(f'P_{i+1}, P_{j+1}, P_{i+1}·P_{j+1}', fontsize=10)
            ax[i,j].legend(fontsize=7)
            ax[i,j].grid(True, alpha=0.3)
            ax[i,j].tick_params(labelsize=7)

    py.savefig('legendre')
    py.show()
    return

#Miscelaneous stuff------------------------------------------------------------------------
def F(g,a,b,u): #This is the transformed function that is to be integrated from -1 to 1
    return g(((b-a)/2)*u + (a+b)/2)*(b-a)/2

def P(n,x):
    return sp.special.legendre(n)(x)

def BisectionRootFinsding(F,lower,upper,value):
    tol = 0.0000000001
    guess = (1/2)*(upper + lower)

    while np.abs(F(guess) - value) > tol:
        if np.sign((F(guess)-value)(F(lower)-value)) == 1:
            lower = guess
            guess = (1/2)*(upper + lower)

        elif np.sign((F(guess)-value)(F(upper)-value)) == 1:
            upper = guess
            guess = (1/2)*(upper + lower)

    return guess

#Program output--------------------------------------------------------------------------------
print("\nThe first thing to examine is the number of subinetervals at which the trapezoidal rule converge to 6 sig figs")

print("\nTrapezoid Rule")
Table(f,0,2,trapezoid(f,0,2,5000000),trapezoid,[2**n for n in range(14)])

print("\n From the table, we see that it reaches 6 digit accuracy somewhere between 4096 and 9192 subintervals.")

print("\nThis is not great. Instead, we can use gaussian quadrature, which achieves higher precision with fewer subintervals.")
print("This algoritm is based on interpolation with legendre polynomials. An important property")
print("is the orthogonality of them. They are plotted below.")

PlotStuff()

print("We can see how much faster gaussian quadrature converges with this table below: ")

print("\nGaussian Quadrature")
Table(f,0,2,GaussQuad(f,0,2,50),GaussQuad,[n+1 for n in range(14)])

print("\nNote that this is signifigantly more accurate at only 25 intervals compared to the thousands of intervals for the trapezoidal rule.")
print("Now, we consider a function with a pole at one of the limits of integration")

print("\nGaussian Quadrature")
Table(g,0,2,np.sqrt(8192)/15,GaussQuad,[2**n for n in range(12)])

print("\nWe can see that this it has a difficult time converging as we increase the number of intervals. Taking several thousand to achieve just 2 sig figs.")
print("We can perform a change of variables and compare this to algorithm that can't handle singularities. The new results are below.")
print("First, we print the reusults for Simpson's rule to compare")

print("\nSimpson's Rule")
Table(G,0,np.pi/2, np.sqrt(8192)/15,Homer,[5*(1+n) for n in range(13)])

print("\nGaussian Quadrature")
Table(G,0,np.pi/2, np.sqrt(8192)/15,GaussQuad,[1+n for n in range(11)])

print("\nNow, gaussian quadrature converges to 10 sig figs in 9 intervals, which is a much better than the untransformed integral and slightly better than the 64 for Simpson's rule.")

    return
    
print(trapezoid(f,0,2,8192))
print(GaussQuad(f,0,2,16))
