#BUKIN FUNCTION N. 6
from math import sqrt
import numpy as np
import random

W = 0.7
c1 = 0.8
c2 = 0.9

n_particulas = 30
interacoes = 1000
erro = 1e-6

class Particle():

    def __init__(self):

        self.posicao = np.array([random.uniform(-1000, 1000),random.uniform(-1000, 1000)])
        self.pbest = self.posicao
        self.pbestvalor = float('inf')
        self.velocidade = np.array([0, 0])

    def update(self):
        return print(f'i am at {self.posicao} , my pbest position is {self.pbest}')

    def move(self):
       self.posicao = self.posicao+self.velocidade



class Space():

    def __init__(self, interacoes, erro, n_particulas):
        self.n_particulas = n_particulas
        self.interacoes = interacoes
        self.erro = erro
        self.particulas = []
        self.gbestvalor =float('inf')
        self.gbest = np.array([random.random() * 100, random.random() * 100])

    def objective_function(self, particula):
        return (100*(sqrt(abs(particula.posicao[1]-0.01*(particula.posicao[0]**2)))))+0.01*abs(particula.posicao[0]+10)

    def move_particles(self):

        for particula in self.particulas:

            new_velocity = (W * particula.velocidade) + (c1 * random.random()) * (particula.pbest - particula.posicao) + (random.random() * c2) \
                                                                                                                             * (self.gbest - particula.posicao)
            particula.velocidade = new_velocity
            particula.move()

    def atualizacao(self):
        for particula in self.particulas:
            particula.update()

    def setpbest(self):
        for particula in self.particulas:
            atualizacao_particula_pbest = self.objective_function(particula)
            if atualizacao_particula_pbest <= particula.pbestvalor:
                particula.pbestvalor = atualizacao_particula_pbest
                particula.pbest = particula.posicao

    def setgbest(self):
        for particula in self.particulas:
            atualizacao_particula_gbest = particula.pbestvalor
            if atualizacao_particula_gbest <= self.gbestvalor:
                self.gbestvalor = atualizacao_particula_gbest
                self.gbest = particula.posicao

space_particles = Space(interacoes, erro, n_particulas)
posicao_aleatoria = [Particle() for i in range(n_particulas)]
space_particles.particulas = posicao_aleatoria

n_interacoes = 0
while n_interacoes < interacoes:
    space_particles.setgbest()
    space_particles.setpbest()
    space_particles.move_particles()
    n_interacoes += 1
    if space_particles.gbestvalor <= erro:
        break

print(space_particles.atualizacao())
print(f'the gbest position is {space_particles.gbest}, and his gbestvalue is { space_particles.gbestvalor}')