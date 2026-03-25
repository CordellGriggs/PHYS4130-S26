from concave_hull import concave_hull
import matplotlib.pyplot as plt
from random import uniform
from shapely.geometry import Polygon

P = [(uniform(0,1),uniform(0,1)) for _ in range(100)]

hull = concave_hull(P, concavity = 1.0)

poly = Polygon(hull)

print(poly.area)

x, y = zip(*P)
xh, yh = zip(*hull)

plt.plot(x,y , 'o')
plt.plot(xh,yh, '-o')
plt.show()
