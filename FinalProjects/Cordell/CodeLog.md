# Code Log
This is for me to commit what I've done code-wise, since I don't want to risk uploading MCNP stuff to github.


I created this starting from 4/28, but I did some coding before then starting Thursday 4/23. Before that I replicated the Godiva sphere and played around with some other geometries.

### 4/28
I created a geometry of concentric cylindrical surfaces with alternating layers of Uranium and water. There seems to be an issue with what I'm calling the inside and/or outside of each surface, so I would like to figure that out before I modify the density of Uranium such that the total Uranium mass in the geometry is 18 kg and estimate $k_{eff}$.

### 4/29
I fixed the bug. The issue is I didn't define a cell inside the inner-most cylinder so it defaulted to void, and my neutrons were spawning at the origin causing them to die instantly as I have it set to not track neutrons in void.

After I fixed the bug I estimated $k_{eff}$ = 1.73 Then, I changed from

CZ: Infinitely long cylindrical surfaces centered on z-axis
--> RCC: "Right circular cylinders" which are a little more involved to define but I can limit their height.

Using the following geometry:
```
c CELL CARDS
10   100  -18.74  +1 -2      imp:n=1                    
20   200  -1.0    +2 -3      imp:n=1                    
30   100  -18.74  +3 -4      imp:n=1                    
40   0            +4         imp:n=0                    
50   200  -1.0    -1         imp:n=1

c SURFACE CARDS
1   RCC     0 0 -50     0 0 100     7.000                                
2   RCC     0 0 -50     0 0 100     14.000
3   RCC     0 0 -50     0 0 100     21.000
4   RCC     0 0 -50     0 0 100     28.000
```

I estimated $k_{eff}$ = 1.70

However, this uses 2885 kg of Uranium. So now I need to shrink the volume of Uranium cells + density of Uranium as to only use 18 kg.

First, I tried taking the density down from 18.74 g/$cm^{3}$ to 0.12 (I did the math and it gave me 18 kg total mass). This gave me $k_{eff}$ = 0.57.

Then, I took the radius down some and bumped up the density. After doing a few rounds of adjustments plus simulations, here are some notable results:

For 9.74 kg total: This geometry I made yields $k_{eff}$ = 0.965. This is around the safety threshold and it only uses a little over half the Uranium they have in stock.

```
Practice 
c CELL CARDS
10   100  -18.74  +1 -2      imp:n=1                   
20   200  -1.0    +2 -3      imp:n=1                    
30   100  -18.74  +3 -4      imp:n=1                    
40   0            +4         imp:n=0                   
50   200  -1.0    -1         imp:n=1

c SURFACE CARDS
1   RCC     0 0 -50     0 0 100     10.000                                   
2   RCC     0 0 -50     0 0 100     10.500
3   RCC     0 0 -50     0 0 100     20.500
4   RCC     0 0 -50     0 0 100     21.000

c DATA CARDS
kcode 10000  1.0  100  200                    
ksrc  0.0  0.0  0.0                           
m100  92235 -.9473                             
      92238 -.0527
m200  1001   2 
      8016   1
```

For 16.1 kg total: This geometry I made yields $k_{eff}$ = 1.06, which achieves the goal of going critical with 18 kg of Uranium.

```
c CELL CARDS
10   100  -18.74  +1 -2      imp:n=1                 
20   200  -1.0    +2 -3      imp:n=1            
30   100  -18.74  +3 -4      imp:n=1        
40   0            +4         imp:n=0       
50   200  -1.0    -1         imp:n=1

c SURFACE CARDS
1   RCC     0 0 -40     0 0 80     10.000                                  
2   RCC     0 0 -40     0 0 80     11.000
3   RCC     0 0 -40     0 0 80     21.000
4   RCC     0 0 -40     0 0 80     22.000

c DATA CARDS
kcode 10000  1.0  100  200                     
ksrc  0.0  0.0  0.0                       
m100  92235 -.9473               
      92238 -.0527
m200  1001   2 
      8016   1
```