import numpy as np
import random
from matplotlib import pyplot as plt


W = 0.7
c1 = 1
c2 = 3
#ajustar self.posicao(nela está ainda os bounds)

class Particle():

    """Cria uma partícula, definindo sua posição com base nos limites e zerando seu pbest e sua velocidade


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

        """"mostra ao usuario a posição atual e o pbest"""

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

class PSO():

    def __init__(self, objective_function,dimensoes, n_particulas, interacoes, erro, boundsmin=[],boundsmax=[], plot='no'):
        """
        Constroi uma matriz com todas as partículas, ajusta a posição caso o exceda a posição limite, verificando os critérios de parada
        e visualiza a função (gbest x numero de interações).


        :param objective_function: float
        Retorna o valor calculado na função baseado nas coordenadas
        :param dimensoes: int
        Dimensão do problema
        :param n_particulas: int
        Número de partículas
        :param interacoes: int
        O número de interações máximo permitido
        :param erro: float
        O erro máximo permitido na convergência
        :param boundsmin: array
        limite mínimos das coordenadas
        :param boundsmax: array
        limite máximo das coordenadas
        :param plot: string('yes', 'no')
        decide se quer plotar ou não
        """
        self.boundsmin = boundsmin
        self.boundsmax = boundsmax
        self.space_particles = Space(interacoes, erro, n_particulas)
        try:
            posicao_aleatoria = [Particle(dimensoes, self.boundsmin, self.boundsmax) for _ in range(n_particulas)]
        except:
            print("não foi definido bound ou o numero de dimensões")
        self.space_particles.particulas = posicao_aleatoria
        n_interacoes = 0
        gbestvalor = []
        vetor_interacoes = []
        while n_interacoes < interacoes:
            self.space_particles.setpbest(objective_function)
            self.space_particles.setgbest()
            self.space_particles.move_particles()
            for particula in self.space_particles.particulas:
                if bool(self.boundsmin) == True:
                    for i in range(len(boundsmin)):
                        if particula.posicao[i] < boundsmin[i]:
                                particula.posicao[i] = boundsmin[i]
                if bool(self.boundsmax) == True:
                    for i in range(len(boundsmax)):
                        if particula.posicao[i] > boundsmax[i]:
                                particula.posicao[i] = boundsmax[i]
                                particula.velocidade= -1*particula.velocidade

            gbestvalor.append(self.space_particles.gbestvalor)
            n_interacoes += 1
            vetor_interacoes.append(n_interacoes)
            if self.space_particles.gbestvalor <= erro:
                break
        memory = n_interacoes*n_particulas
        if bool(self.boundsmin) == False:
            print('o problema não possui restrição minima')
        if bool(self.boundsmin) == False:
            print('o problema não possui restrição maxima')
        print(self.space_particles.atualizacao())
        print(f'the gbest position is {self.space_particles.gbest}, and his gbestvalue is {self.space_particles.gbestvalor}, a memória {memory}')
        if plot == 'yes':
            plt.plot(vetor_interacoes, gbestvalor)
            plt.xlabel('n_interações')
            plt.ylabel('gbest')
            plt.show()
