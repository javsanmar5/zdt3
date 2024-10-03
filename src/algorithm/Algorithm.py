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
        self.ER = 0.2
        self.F = 0.5
        self.CR = 0.4
        self.search_space = (0, 1)
        
        # self.population = [[random.random() for _ in range(self.n)] for _ in range(self.individuals)]
        # INITIALIZE POPULATION
        self.population = [np.random.rand(self.n) for _ in range(self.individuals)]
        self.z = [min(zdt3(individual)[i] for individual in self.population) for i in range(self.m)]
        self.subproblems = self._initialize_subproblems()

    def _initialize_subproblems(self) -> list[Subproblem]:
        subproblems = []
        lambda1, lambda2 = 1., 0.
        delta = 1 / (self.individuals - 1)
        for _ in range(self.individuals):
            subproblems.append(Subproblem(lambdas=(lambda1, lambda2)))
            lambda1 -= delta
            lambda2 += delta
        for i in range(len(subproblems)):
            subproblem = subproblems[i]
            subproblem.set_neighborhood(subproblems, self.T)
            subproblem.set_best_solution(self.population[i])
            subproblem.set_solution_fitness(self._g_te(lambdas= subproblem.lambdas ,F_y=zdt3(self.population[i])))

        return subproblems
    
    def _update_z(self, F_y: list) -> None:
        for i in range(self.m):
            self.z[i] = min(self.z[i], F_y[i])
    

    # --------------- EVOLUTIONARY OPERATORS ---------------
    
    # Abstraction layer
    def generate_new_individual(self, i: int) -> np.ndarray[np.float64]:
        mutant = self._mutate(i)  
        trial = self._crossover(self.population[i], mutant)  
        return min((mutant, trial, self.population[i]), key=lambda x: self._g_te(lambdas= self.subproblems[i].lambdas, F_y=zdt3(x)))

    def _mutate(self, i: int) -> np.ndarray:
        a, b, c = random.sample(self.subproblems[i].neighborhood, 3)
        mutated = self.population[a] + self.F * (self.population[b] - self.population[c])
        mutated = np.clip(mutated, self.search_space[0], self.search_space[1])
        return mutated
    
    def _crossover(self, parent: np.ndarray, mutant: np.ndarray) -> np.ndarray:
        trial = np.copy(parent)
        for i in range(self.n):
            if random.random() < self.CR:
                trial[i] = mutant[i]
        return trial


    
    
    # ------------------- EVALUATION -------------------       

    # @staticmethod        
    # def _g_te(m: int, lambdas: list, F_y: list, z: list) -> float:
    #     maximum_value = 0
    #     for j in range(m):
    #         maximum_value = max(maximum_value, lambdas[j] * abs(F_y[j] - z[j]))
    #     return maximum_value
    
    
    def _g_te(self, lambdas,  F_y):
        maximum_value = float("-inf")
        for j in range(self.m):
            maximum_value = max(maximum_value, lambdas[j] * abs(self.z[j] - F_y[j]))
        return maximum_value
        
    # ------------------- MAIN LOOP -------------------       
     
    def run(self):
        acum_f = []
        iteration = 0
        while iteration < self.iterations:
            next_population = [0. for _ in range(self.individuals)]
            for i in range(self.individuals):
                
                y = self.generate_new_individual(i)
                next_population[i] = y
                
                F_y = zdt3(y)
                
                self._update_z(F_y)
                
                for subproblem in self.subproblems[i].neighborhood:
                    current_g_te= self._g_te(lambdas= self.subproblems[subproblem].lambdas, F_y=F_y)
                    if current_g_te < self.subproblems[subproblem].solution_fitness:
                        self.subproblems[subproblem].set_best_solution(y)
                        self.subproblems[subproblem].set_solution_fitness(current_g_te)
                    # elif random.random() < self.ER:
                    #     next_population[i] = self.subproblems[subproblem].best_solution
                
                # for j in self.subproblems[i].neighborhood:
                #     current_g_te = Algorithm._g_te(self.m, self.subproblems[j].lambdas, F_y, self.z)
                #     if current_g_te < self.subproblems[j].solution_fitness:
                #         self.subproblems[j].set_best_solution(y)
                #         self.subproblems[j].set_solution_fitness(current_g_te)
                        
                # print(f"{i}: {self.subproblems[i].best_solution} -> {zdt3(self.subproblems[i].best_solution)}")

                acum_f.append((F_y, 0))
                # acum_f.append((zdt3(self.subproblems[i].best_solution), 0))

                # print(f"{i}: {self.subproblems[i].best_solution} -> {zdt3(self.subproblems[i].best_solution)}")
                # if iteration <= 2:
                #     print(self.subproblems[i])
                
            self.population = next_population

            iteration += 1
            
        return acum_f
                