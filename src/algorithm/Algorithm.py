import random

import numpy

from algorithm.Subproblem import *
from zdt3.zdt3_function import zdt3


class Algorithm:

    def __init__(self, iterations: int, individuals: int) -> None:
        self.iterations = iterations
        self.individuals = individuals

        self.n = 30 # Number of dimensions
        self.m = 2 # Number of objectives
        
        # PARAMETERS
        self.T = int(0.2 * self.individuals)
        self.MR = 0.1
        self.F = 0.5
        self.CR = 0.5
        
        self.population = [[random.random() for _ in range(self.n)] for _ in range(self.individuals)]
        self.evals = [zdt3(individual) for individual in self.population]
        self.z = [min([evals[i] for evals in self.evals]) for i in range(self.m)]
        self.subproblems = self._initialize_subproblems()
        
    def _initialize_subproblems(self) -> list[Subproblem]:
        subproblems = []
        lambda1, lambda2 = 0., 1.
        delta = 1 / self.n - 1
        for _ in range(self.n):
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
        elif F_y[1] < self.z[1]:
            self.z[1] = F_y[1]
    

    # --------------- EVOLUTIONARY OPERATORS ---------------
    
    def _mutate(self, i: int, F: float) -> None:
        x_r1, x_r2, x_r3 = random.sample(self.subproblems[i].neighborhood, 3)
        new_individual = [
            max(0, min(1, self.population[x_r1][j] + F * (self.population[x_r2][j] - self.population[x_r3][j])))
            for j in range(self.n)
        ]
        self._crossover(self.population[i], new_individual, self.CR)

    def _crossover(self, x: list, v: list, CR: float) -> None:
        for j in range(self.n):
            if random.random() <= CR:
                x[j] = max(0, min(1, v[j]))  


    # ------------------- EVALUATION -------------------       

    def fitness(self, lambdas: list, F_y: list) -> float: # Abstraction layer
        return Algorithm._g_te(self.m, lambdas, F_y, self.z)
        
    @staticmethod        
    def _g_te(m: int, lambdas: list, F_y: list, z: list) -> float:
        maximum_value = 0
        for j in range(m):
            maximum_value = max(maximum_value, lambdas[j] * abs(F_y[j] - z[j]))
        return maximum_value
    
        
    # ------------------- MAIN LOOP -------------------       
     
    def run(self):
        iteration = 0
        while iteration < self.iterations:
            for i in range(self.individuals):
                self._mutate(i, self.F)
                y = self.population[i]
                F_y = zdt3(y)
                self._update_z(F_y)
                if self.fitness(self.subproblems[i].lambdas, F_y) < self.subproblems[i].solution_fitness:
                    self.subproblems[i].set_best_solution(y)
                    self.subproblems[i].set_solution_fitness(self.fitness(self.subproblems[i].lambdas, F_y))
            iteration += 1
            
        return [zdt3(subproblem.best_solution) for subproblem in self.subproblems]
                
                