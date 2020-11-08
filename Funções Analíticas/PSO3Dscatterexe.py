from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from PSO3DScatter import PSO3d
from scatter_interacoesgbest import PSO

def objective_function(x):
    value = (x[0] ** 2 + x[1] - 11) ** 2 + (x[0] + x[1] ** 2 - 7) ** 2
    return value


PSO3d(objective_function, 2, 30, 200, 1e-6, boundsmin=[-6, -6], boundsmax=[6, 6], plot='yes')

"""2D SCATTER
plt.scatter(vetor_interacoes, gbestvalor)
plt.xlabel('n_interações')
plt.ylabel('gbest')
plt.show()"""

"""GBEST 3D
x = [np.linspace(-6, 6, 30), np.linspace(-6, 6, 30)]
X = np.meshgrid(x[0], x[1])
Z = objective_function(X)
ax = plt.axes(projection='3d')
ax.contour3D(X[0], X[1], Z, 50, cmap='viridis')

X1 = [i[0] for i in gbestparticles]
X2 = [i[1] for i in gbestparticles]
H = []
for i in gbestparticles:
    H.append(objective_function(i))
ax.scatter(X1, X2, H, cmap='binary')  # binario é pra duas cores e o 50 é se é mais denso o grafico

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()"""

"""PARTICULAS 3D
x = [np.linspace(-6, 6, 30), np.linspace(-6, 6, 30)]
X = np.meshgrid(x[0], x[1])
Z = objective_function(X)
ax = plt.axes(projection='3d')
ax.contour3D(X[0], X[1], Z, 50, cmap='viridis')  # binario é pra duas cores e o 50 é se é mais denso o grafico
Z = []
for particula in particulas:
    Z.append(objective_function(particula))
ax.scatter(particulas[0], particulas[1], Z, cmap='binary')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()"""