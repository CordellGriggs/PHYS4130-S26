# Introduction

## Background Theory

# Procedure 

## Ultimate DLA Simulation Code

### Changelog Summary
The code described above took a long time to optimize the runtime for large N. Below, we share the trials and errors that led up to the code above.
#### Periodic Boundary Conditions
The first big thing we implemented was periodic boundary conditions to prevent the particles from wandering too far away from the seed. We implemented this using the mod operator as shown below:
``` python
        direction = np.random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up':
            y = (y + 1) % length
        elif direction == 'down':
            y = (y - 1) % length
        elif direction == 'left':
            x = (x - 1) % length
        elif direction == 'right':
            x = (x + 1) % length
```


#### Resizing Boundary
Initially, we also started with a 100 block square spawn parameter centered around the seed. After running a simulation with 1000? particles we observed that the particles accumulated on the edges as they spawned in which is not realistic as the spawn parameter just represents the income of the particles at that point--- they don't just spawn there out of thin air. So, we increased N to avoid this; however, increasing N resulted in a much longer run time since the particles took longer to walk further to the seed. So, then we implemented the resizing functions to keep the spawn parameter at a balanced distance from the seed. The distance was chosen to be 3 times the radius of the aggregate point furthest from the origin. 

```python
def resizing():
    ##############################################
    # Adaptive resizing
    global length, space, heat                                          # I should probably pass these later but rn Im just testing stuff
    
    r_max = np.max(np.abs(np.argwhere(space) - length//2)) + 1          # max distance from the center seed
    if length < 3 * r_max:                                              # condition to adjust length
        new_length = 3 * r_max
        if new_length % 2 == 0:                                         # ensures new length is odd so seed can remain centered
            new_length += 1

        new_space = np.zeros((new_length, new_length), dtype=bool)      # adjusts space to new length dimensions
        new_heat = np.zeros((new_length, new_length))                   # adjusts heat to new length dimensions

        shift = (new_length - length) // 2                              # shift such that the space expands outwards from center

        crystal_indices = np.argwhere(space)                            # ^ adjusts space such that it adds space outwards from center
        for x, y in crystal_indices:
            new_space[x + shift, y + shift] = True
            new_heat[x + shift, y + shift] = heat[x, y]
        
        length = new_length                                             # updates length
        space = new_space                                               # updates space
        heat = new_heat                                                 # updates heat

    ##############################################
```

#### Circular Spawn Parameter
Yet, we still weren't satisfied with the runtime, so we changed the shape of the spawn parameter to a circle instead of a square. This change allowed us to spawn particles closer to the crystal. To visualize this, imagine two concentric squares where the particles pass into the exterior square in a uniformly distributed manner and take random walks. They will not pass through the interior square in a uniformly distributed manner. Meanwhile, for a pair of concentric circles, if the particles pass into the exterior circle in a uniformly distributed manner then they will pass through the interior circle uniformly. Naturally, we also wrote a resizing function for the circle which was based of the maximum distance of a crystal point from the center plus 10.

```python
def generate_space(radius):
    num_edge_blocks = int(2 * np.pi * radius)                                                               # num edge blocks is the integer value of circumerence
    theta = np.linspace(0, 2 * np.pi, num_edge_blocks, endpoint=False)                                      # generates num_edge_blocks angles evenly spaced around the circle
    x, y = np.round(radius * np.cos(theta)).astype(int), np.round(radius * np.sin(theta)).astype(int)       # finds the x and y positions of the points on the circle
    return x, y

x, y = generate_space(radius)
circle_set = np.unique(np.column_stack((x, y)), axis=0)         # pairs x and y defines the circle (np.unique removes any duplicates due to rounding)
```


#### Spawn Function
The early versions of the spawn function would define a segmented curve and pick a random point on that curve. We later changed this to pick a random angle at the set radius which is faster.
```python
def spawn(radius):
    theta = np.random.uniform(0, 2 * np.pi)                                                                 # generates a random angle between 0 and 2pi
    x, y = int(radius * np.cos(theta)), int(radius * np.sin(theta))
    return x, y
```

#### Checking r_max
Initially, we were checking the max radius by using np.max to sift through the distance of each point on the crystal for every loop of N. We improved the efficiency of this search by storing the initial r_max and every new point we check if its greater than the current r_max, and if so, we update r_max.

#### Random Walk Algorithm
Initially, we were using np.random.choice to choose up, down, left or right. We later changed this to np.random.randint which is faster.

#### Neighborhood Check
Initially we were slicing the neighborhood with
```python
        if (space[x-1:x+2, y-1:y+2].any()):
```
yet we found that 
```python
        if 0 < x < length - 1 and 0 < y < length - 1:                           # only checks if particle is not on the edge to avoid errors (aggregate does not approach edge so this is fine)
            if (space[x-1, y-1] or space[x-1, y] or space[x-1, y+1] or          # checks 3x3 neighborhood for crystal
                space[x,   y-1] or space[x,   y] or space[x,   y+1] or
                space[x+1, y-1] or space[x+1, y] or space[x+1, y+1]):
```
is more efficient. 

#### New Boundary Conditions
We found that making the particles bounce off the walls was more efficient than using periodic boundary conditions. And they are parity symmetric so it doesn't change much. 

```python
        # RANDOM WALK ALGORITHM
        direction = np.random.randint(4)

        # particles bounce off walls instead of periodic BC but its effectively the same.
        if direction == 0:        
            if y < length - 1:
                y += 1
        elif direction == 1:
            if y > 0:
                y -= 1
        elif direction == 2:
            if x > 0:
                x -= 1
        else:
            if x < length - 1:
                x += 1
```


# Analysis 

# Conclusions