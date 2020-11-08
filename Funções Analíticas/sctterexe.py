from scatter_interacoesgbest import PSO
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
def objective_function(x):
    value = (x[0] ** 2 + x[1] - 11) ** 2 + (x[0] + x[1] ** 2 - 7) ** 2
    return value

PSO(objective_function,2, 30, 200, 1e-6, boundsmin=[-6, -6], boundsmax=[6, 6])
