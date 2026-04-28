## Intro
dummy intro
There are PDEs that must be solved. But, they don't want to be solved. However, mathematicians are clever. THey found a way to solve problems that don't want to be solved!
## Algorithms and Theory
a) There is a hihgly intuitive way of numerically solving PDEs. 
  I) We are able to discretize spatial derivativres over our spatial domain and create a 
     large system of coupled ODEs since the approximation of the spatial derivatives
     mixes discretized terms.
  II) Then, we can churn this system of ODEs through a numeerical method such as RK45 
      and create a numerical solution. 
  III) Here, show a plot of a sample simulation that I can animate
b) That method is fine enough for simple PDEs, but if you want to do something 
   more complicated then you need a more sophisticated method. If we want to solve something
   like the Kuramoto-Sivashinksy equation (which is 4th order in space and nonlinear) then the old method
   won't cut it. Instead, we can use Exponential Time Difference RK4 (ETDRK4)
   I) Explaining the method: We want to solve a PDE of the form 
```math
\partial_t u = Lu + N(u)
```
  Where L is a linear (but possibly stiff) operator and N(u) is nonlinear. 

  II) Then, if L is a differential operator, and we solve our problem over periodic BCs, then we can write our funciton as a fourier expansion
```math
u(x,y,t) = \sum_{k_x , k_y} A_{k_x, k_y}(t) e^{i(k_x  x + k_y  y)},
```
  and L is now a diagonal operator in the sense that u is represented in the eigenbasis of L. 
  Let 
```math
\hat{u(t)} = \begin{pmatrix} A_{k_x, k_y}(t) \end{pmatrix}_{k_x, k_y wave numbers}
```
  be the fourier space representation of u. 
  III) Let h be a timestep. We now introduce an integrating factor
```math
w(x,y,t) = e^{-Lh}.
```
  Recall that the matrix exponential is itself an operator. This allows us to derive an exact time step formula.
  (Skipping steps here to get to the time step formula)
```math
u(x,y, t+h) = e^{Lh}u(x,y,t) + e^{Lh} \int_{0}^{h} e^{-L\tau} N(u(x,y,t+\tau)d\tau.
```
This formula is exact, and the RK4 part comes in how we approximate this integral (not included here atm)
We need the fourier space representation for the efficient computation of matrix exponentials. 

# Solving the Kuramoto Sivashinksy Equation
Derive the particular update formula for ETDRK4 here for the KS equation. Show pretty plots, and the python implementation here.
  
  
