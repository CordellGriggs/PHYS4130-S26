# Alec Training Notes

## Imports
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
```
- `pandas` is used for data manipulation and analysis.
- `numpy` is used for numerical operations and handling arrays.
- `matplotlib.pyplot` is used for plotting and visualizing data.
- `torch` is the main library for building and training neural networks.
- `torch.nn` is a sub-library of PyTorch that provides modules and classes for building neural networks.

## Input Domains
The input domains for our model will depend on the specific problem we are trying to solve. For example, if we are working on a classification problem, our input domain might consist of features such as age, income, and education level. If we are working on a regression problem, our input domain might consist of features such as temperature, humidity, and time of day.

```python
x_data = torch.linspace(0,1,5).view(-1,1)
x_col  = torch.rand(100,1)
x_test = torch.linspace(0,1,20).view(-1,1)
```

| Variable | Purpose | Description | Notes |
|----------|---------|-------------|-------|
| `x_data` | Training data points | A tensor containing the training data points, generated using `torch.linspace`. | 5 fixed points in [0,1] |
| `x_col`  | Random data points   | A tensor containing random data points, generated using `torch.rand`. | 100 random points |
| `x_test` | Test data points     | A tensor containing the test data points, generated using `torch.linspace`. | 20 fixed points in [0,1] for plotting |

### Note
```python
.view(-1,1)
```
The `.view(-1,1)` method is used to reshape the tensor. In this case, it reshapes the tensor into a 2D tensor with one column and as many rows as needed (determined by the number of elements in the original tensor). This is often done to ensure that the data is in the correct format for input into a neural network.

## Dummy Zero Function
```python
z = lambda x: np.zeros_like(x.numpy())
```
The `z` function is a dummy function that takes a tensor `x` as input and returns a tensor of the same shape filled with zeros. The `np.zeros_like` function creates an array of zeros with the same shape and type as the input array. The `.numpy()` method is used to convert the PyTorch tensor to a NumPy array before passing it to `np.zeros_like`. This function can be useful for initializing certain parameters or for testing purposes.

## Visualization
```python
plt.scatter(x_data.numpy(), z(x_data), marker='*', s=50, label='data', color='red')
plt.scatter(x_col.numpy(),  z(x_col),  s=10, label='col')
plt.scatter(x_test.numpy(), z(x_test), marker='x', s=10, label='test', color='k')
```
This code snippet creates a scatter plot to visualize the data points.
- The first `plt.scatter` plots the training data points (`x_data`) as red stars.
- The second `plt.scatter` plots the random data points (`x_col`) as small points.
- The third `plt.scatter` plots the test data points (`x_test`) as black crosses.

## Define Target Function
```python
u_data = torch.exp(-x_data)
```
This line defines the target function `u_data` as the exponential of the negative of `x_data`. The `torch.exp` function computes the exponential of each element in the input tensor. This means that for each value in `x_data`, we are calculating `e^(-x)`, which will give us a curve that decays as `x` increases. This target function can be used for training a model to learn the relationship between `x_data` and `u_data`.

## Plotting Training Data
```python
plt.scatter(x_data.numpy(), u_data.numpy(), label="Training data")
```
This line of code creates a scatter plot of the training data points. It plots `x_data` on the x-axis and `u_data` on the y-axis. The `label` parameter is set to "Training data", which will be used in the legend to identify this set of points. The `.numpy()` method is used to convert the PyTorch tensors to NumPy arrays for plotting with Matplotlib.

## Define Neural Network Model
```python
class PINN(nn.Module):
```



