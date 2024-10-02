import random

import numpy as np

from algorithm.Subproblem import *
from zdt3.zdt3_function import zdt3


class Algorithm:

    def __init__(self, iterations: int, individuals: int) -> None:
        self.iterations = iterations
        self.individuals = individuals

        self.n = 30 # Dimensions
        self.m = 2 # Objectives
        
        # PARAMETERS
        self.T = int(0.3 * self.individuals)
        self.MR = 0.1
        self.F = 0.5
        self.CR = 0.5
        self.search_space = (0, 1)
        
        # self.population = [[random.random() for _ in range(self.n)] for _ in range(self.individuals)]
        # INITIALIZE POPULATION
        self.population = [np.random.rand(self.n) for _ in range(self.individuals)]
        self.z = [float("inf") for _ in range(self.m)]
        self.subproblems = self._initialize_subproblems()

    def _initialize_subproblems(self) -> list[Subproblem]:
        subproblems = []
        lambda1, lambda2 = 0., 1.
        delta = 1 / (self.individuals - 1)
        for _ in range(self.individuals):
            subproblems.append(Subproblem(lambdas=(lambda1, lambda2)))
            lambda1 += delta
            lambda2 -= delta
        for i in range(len(subproblems)):
            subproblem = subproblems[i]
            subproblem.set_neighborhood(subproblems, self.T)
            subproblem.set_best_solution(self.population[i])
            subproblem.set_solution_fitness(Algorithm._g_te(self.m, subproblem.lambdas, zdt3(self.population[i]), self.z))

        return subproblems
    
    def _update_z(self, F_y: list) -> None:
        if F_y[0] < self.z[0]:
            self.z[0] = F_y[0]
        if F_y[1] < self.z[1]:
            self.z[1] = F_y[1]
    

    # --------------- EVOLUTIONARY OPERATORS ---------------
    
    def _mutate(self, i: int) -> None:
        x_r1, x_r2, x_r3 = random.sample(self.subproblems[i].neighborhood, 3)
        new_individual = np.clip(self.population[x_r1] + self.F * (self.population[x_r2] - self.population[x_r3]), self.search_space[0], self.search_space[1])
        self._crossover(self.population[i], new_individual, self.CR)

    def _crossover(self, x: list, v: list, CR: float) -> None:
        for j in range(self.n):
            if random.random() <= CR:
                x[j] = max(self.search_space[0], min(self.search_space[1], v[j]))  


    # ------------------- EVALUATION -------------------       

    @staticmethod        
    def _g_te(m: int, lambdas: list, F_y: list, z: list) -> float:
        maximum_value = 0
        for j in range(m):
            maximum_value = max(maximum_value, lambdas[j] * abs(F_y[j] - z[j]))
        return maximum_value
    
        
    # ------------------- MAIN LOOP -------------------       
     
    def run(self):
        acum_f = []
        iteration = 0
        while iteration < self.iterations:
            for i in range(self.individuals):
                self._mutate(i)
                y = self.population[i]
                F_y = zdt3(y)
                self._update_z(F_y)
                for j in self.subproblems[i].neighborhood:
                    current_g_te = Algorithm._g_te(self.m, self.subproblems[j].lambdas, F_y, self.z)
                    if current_g_te < self.subproblems[j].solution_fitness:
                        self.subproblems[j].set_best_solution(y)
                        self.subproblems[j].set_solution_fitness(current_g_te)
                print(self.subproblems[1].solution_fitness)
                print(self.subproblems[1].lambdas)
                acum_f.append(zdt3(self.subproblems[i].best_solution))
            iteration += 1
            
        return acum_f
        print(self.subproblems)
        return [zdt3(subproblem.best_solution) for subproblem in self.subproblems]
                
                