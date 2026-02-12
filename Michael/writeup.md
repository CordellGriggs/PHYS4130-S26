
Project 1 
==

Attribution
--
The primary resources for this assignment were the previous jupyter notebooks for numeric integration. THey contained useful examples of looping, plotting, and other relevant syntax for python. When they did not suffice, internet resources were used. For example, if I wanted to learn how to format an axis in a plot with pylab, I would search something to the effect of "How to format axes in pylab?" and then usually the first few results would have the information I needed. 

Timekeeping
---
I would estimate I spent around three to four hours on this

Languages, Libraries, Lessons Learned 
---
The only language use was python becuase thus far everything has been in python. I only know it and C++, and I did not want to use C++. The libraries were numpy, scipy, and matplotlib.pyplot. The first two were simple to use. However, I had trouple getting the plotting to work because I didn't know I had to import matplotlib.pyplot and not just matplotlib.

Examminations of the Code
---
The trapezoidal rul achieved accuracy of 10^-6 at approximatley 8192 intervals. This is consisten with the results from numerical analysis becuase this method has an error order of O(h^2), meaning that the error decreases quadratically as the step size decreases.

The trapezoidal rule essentially uses a linear approximation of function on a subinterval to compute area. Similarly, Simpson's rule instead uses quadratics which allows for a more accurate approximation and thus faster convergence. Then, we will consider a new method called Gaussian Quadrature. The basis of the approximations for this method are the Legendre polynomials.

As a refresher, the Legendre polynomials are a set of polynomials that are orthogonal on the interval [-1,1]. The first four are plotted below, as well as their products. The plots depict that Pn * Pm = d(n,m).

![Legendre Polynomials](legendre.png)

Then, the gaussian quadrature algorthim works by assuming a general structure for an integration method:

I=∫ab​f(x)dx ≈ i=∑​wi​f(xi​) where wi is the weight and xi is the sampling point

Instead of evenly spaced sampling points, or 'nodes', we instead search for a way to optimize the amount of nodes we have and the associated weights to best approximate the integral. To take advantage of the orthogonality of Legendre polynomials, we map the integral from the interval [a,b] to [-1,1] using the change of varaibles

 u = (2x - a - b) / (b - a)

 We can confirm:
 u(a) = (a-b)/(b-a) = -1
 u(b) = (b - a)/(b - a) = 1

 and, we also have that du = 2/(b-a)

 This allows us to convert the intgral into the new form:

 ∫[a,b] ​f(x)dx = ∫[-1,1] f((b-a)/2)*u + (a+b)/2)*(b-a)/2)du 

 Now, we expand f(x) over the legendre polynomials up to a desired order n

 f(x)=k=∑​ak​Pk​(x), where ak are derived with the inner product.

 This approximation is exact for polynomials up to degree 2n-1, and we will use that construct the gaussian qudrature algortihm. We take out sampling points to be the zeros of the nth legenrdre polynomial. Then, divide a polynomial of degree 2n-1 by Pn(x). Thus, we can use the remainder theorem to write the polynomials in the pollowign form:

 p(x) = q(x)*Pn(x) + r(x), where q(x) is the quotient and r(x) is the remainder.

 Then, ∫[-1,1]q(x)Pn​(x)dx = 0 since q(x) is of a lower degree than Pn(x). 

 Therefore, 

∫p(x)dx = ∫r(x)dx and p(xi) = r(xi)

Thus, we are now ready to start determining the weights for our sum. We have from the previous equalty that:

∑wi​p(xi) = ∑wi​r(xi​) = ∫p(x)dx since we are forcing the method to converge exactly for polynomials of deg n-1

We then have from the exactness that blah blah blah I will finish this later...

Then, the available packages in python allow you to implement this algortihm in about three lines: 

def GaussQuad(g,a,b,N):
    roots, weights = sp.special.roots_legendre(N)
    return np.sum([weights[i]*g(((b-a)/2)*roots[i] + (a+b)/2)*(b-a)/2 for i in range(N)])

This function takes in the real valued function g and integrates it over the interval [a,b] using Nth order gaussian quadrature. The first line grabs the roots and weights. The return statement is compactly written to compute the sum that will approximate the integral.

This algortithm is signifigantly faster at computing integrals than the trapezoidal rule. The trapezoidal rule takes nontrivial amount of time to compute the prvious integral from [-1,1] to 6 digit precision. For a similar computation time, this algorithm acheives a greater precision.






