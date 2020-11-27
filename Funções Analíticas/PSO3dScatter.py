# Created by Leonardo Maciel-UFPE-
# Himmelblau function
from math import sqrt
import numpy as np
import random
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
#constantes globais do programa
W = 0.7
c1 = 0.8
c2 = 0.9

class Particle():

    """
    Cria uma partícula, definindo sua posição com base nos limites e zerando seu pbest e sua velocidade

    Parâmetros
    ------
    dimensoes: int
        dimensão da partícula
    boundsmin: array
        limite mínimos das coordenadas
    boundsmax: array
        limite máximo das coordenadas
    """

    def __init__(self, dimensoes, boundsmin = [], boundsmax = []):
        self.boundsmin = boundsmin
        self.boundsmax = boundsmax
        self.dimensoes = dimensoes
        self.posicao = np.random.uniform(low=self.boundsmin, high=self.boundsmax, size=self.dimensoes)
        self.pbest = self.posicao
        self.pbestvalor = float('inf')
        self.velocidade = np.zeros_like(self.posicao)


    def update(self):

        """mostra ao usuario a posição atual e o pbest"""

        return print(f'i am at {self.posicao} , my pbest position is {self.pbest}')


    def move(self):

        """atualiza a posição da particula"""

        self.posicao = self.posicao + self.velocidade

class Space():

    """Itera as partículas"""

    def __init__(self, interacoes, erro, n_particulas):
        """
        Inicializando os valores de posição, gbest e pbest

        :param interacoes: int
        O número de interações máximo permitido
        :param erro: float
        O erro máximo permitido na convergência
        :param n_particulas: int
        Número de partículas
        """
        self.n_particulas = n_particulas
        self.interacoes = interacoes
        self.erro = erro
        self.particulas = []
        self.gbestvalor = float('inf')
        self.gbest = np.array([random.random() * 100, random.random() * 100])


    def move_particles(self):

        """atualiza a velocidade da particula e muda a posição da partícula com a função move"""

        for particula in self.particulas:
            new_velocity = (W * particula.velocidade) + (c1 * random.random()) * (
                        particula.pbest - particula.posicao) + (random.random() * c2) \
                           * (self.gbest - particula.posicao)
            particula.velocidade = new_velocity
            particula.move()


    def atualizacao(self):

        """mostra ao usuario a posição e o pbest atualizados"""

        for particula in self.particulas:
            particula.update()


    def setpbest(self, objective_function):

        """atualiza o pbest"""

        for particula in self.particulas:
            atualizacao_particula_pbest = objective_function(particula.posicao)
            if atualizacao_particula_pbest < particula.pbestvalor:
                particula.pbestvalor = atualizacao_particula_pbest
                particula.pbest = particula.posicao


    def setgbest(self):

        """atualiza o gbest"""

        for particula in self.particulas:
            atualizacao_particula_gbest = particula.pbestvalor
            if atualizacao_particula_gbest < self.gbestvalor:
                self.gbestvalor = atualizacao_particula_gbest
                self.gbest = particula.posicao

class PSO3d():

    """constroi uma matriz com todas as partículas, ajusta a posição caso exceda a posição limite, verifica os critérios de parada
    e visualiza a função e os ultimos resultados obtidos por cada partícula.


    Parâmetros
    -----
    objective_function: float
        Retorna o valor calculado na função baseado nas coordenadas
    dimensoes: int
        dimensões do problema
    n_particulas: int
        Número de partículas
    interacoes: int
        O número de interações máximo permitido
    erro: float
        O erro máximo permitido na convergência
    boundsmin: array
        limite mínimos das coordenadas
    boundsmax: array
        limite máximo das coordenadas
    plot: string('yes', 'no')
        decide se quer plotar ou não"""

    def __init__(self, objective_function, dimensoes, n_particulas, interacoes, erro, boundsmin=[], boundsmax=[], plot='no'):

        self.boundsmin = boundsmin
        self.boundsmax = boundsmax
        self.space_particles = Space(interacoes, erro, n_particulas)
        try:
            posicao_aleatoria = [Particle(dimensoes, self.boundsmin, self.boundsmax) for _ in range(n_particulas)]
        except:
            print("não foi definido bound ou o numero de dimensões")
        self.space_particles.particulas = posicao_aleatoria
        n_interacoes = 0
        gbestparticles = []
        #ajusta a posição caso o exceda a posição limite e verifica os critérios de parada a partir daqui
        while n_interacoes < interacoes:
            particulas = []
            self.space_particles.setpbest(objective_function)
            self.space_particles.setgbest()
            self.space_particles.move_particles()
            for particula in self.space_particles.particulas:
                if bool(self.boundsmin) == True:
                    for k in range(len(boundsmin)):
                        if particula.posicao[k] < boundsmin[k]:
                            particula.posicao[k] = boundsmin[k]
                if bool(self.boundsmax) == True:
                    for j in range(len(boundsmax)):
                        if particula.posicao[j] > boundsmax[j]:
                            particula.posicao[j] = boundsmax[j]
                            particula.velocidade = -1 * particula.velocidade
            #ultima posição das partículas e todos os gbests ao longo da interação
                particulas.append(particula.posicao)
            gbestparticles.append(self.space_particles.gbest)
            n_interacoes += 1

            if self.space_particles.gbestvalor < erro:
                break

        if bool(self.boundsmin) == False:
            print('o problema não possui restrição minima')
        if bool(self.boundsmin) == False:
            print('o problema não possui restrição maxima')
        print(self.space_particles.atualizacao())
        print(f'the gbest position is {self.space_particles.gbest}, and his gbestvalue is {self.space_particles.gbestvalor}')

        if plot == 'yes':
            #representando a função
            if bool (self.boundsmin) == True:
                x = [np.linspace(self.boundsmin[0], self.boundsmax[0], 30), np.linspace(self.boundsmin[1], self.boundsmax[1], 30)]
            else:
                x = [np.linspace(-1000, 1000, 30), np.linspace(-1000, 1000, 30)]
            X = np.meshgrid(x[0], x[1])
            Z = objective_function(X)
            ax = plt.axes(projection='3d')
            ax.contour3D(X[0], X[1], Z, 50, cmap='viridis')


            #coloca a posição x e y em uma variável, respectivamente
            X1 = [i[0] for i in particulas]
            X2 = [i[1] for i in particulas]
            Z = []
            for particula in particulas:
                Z.append(objective_function(particula))
            ax.scatter(X1, X2, Z, cmap='binary')  # binario é pra duas cores

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            plt.show()


        '''TODAS AS PARTICULAS
        x = [np.linspace(-6, 6, 30), np.linspace(-6, 6, 30)]
        X = np.meshgrid(x[0], x[1])
        Z = objective_function(X)
        ax = plt.axes(projection='3d')
        ax.contour3D(X[0], X[1], Z, 50, cmap='viridis')

        X1=[i[0] for i in particulas]
        X2 = [i[1] for i in particulas]
        Z=[]
        for particula in particulas:
            Z.append(objective_function(particula))
        ax.scatter(X1,X2, Z, cmap='binary')  # binario é pra duas cores e o 50 é se é mais denso o grafico

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.show()'''