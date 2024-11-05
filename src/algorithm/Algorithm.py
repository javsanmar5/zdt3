import math
import random

import numpy as np

from functions.cf6_function import cf6, constraints_cf6
from functions.zdt3_function import constraints_zdt3, zdt3


class Algorithm:

    def __init__(self, function: str, iterations: int, individuals: int, **kwargs) -> None:
        self.function = function
        self.iterations = iterations
        self.individuals = individuals

        self.n = 30 if function == "zdt3" else kwargs.get("n", 4)
        self.m = 2 
        self.search_space = (0, 1) if function == "zdt3" else (-2, 2)


        # PARAMETERS
        self.T = kwargs.get("T", int(0.3 * self.individuals))
        self.MR = kwargs.get("MR", 1 / self.individuals)
        self.F = kwargs.get("F", 0.5)
        
        self.CR = kwargs.get("CR", 0.5)
        self.PR = kwargs.get("PR", 1 / self.n)
        
        # INITIALIZE POPULATION
        self.population = [self._initialize_individual() for _ in range(self.individuals)]
        self.F_y = [self.calculate_F(individual) for individual in self.population]
        self.constraints = [self.calculate_constraints(individual) for individual in self.population]

        self.lambdas = self._initialize_lambdas()
        self.neighborhood = self.initialize_neighborhood()
        self.z = [min(f[j] for f in self.F_y) for j in range(self.m)]


    # -------------- AUXILIAR INITIALIZATION --------------

    def _initialize_lambdas(self):
        lambdas = []
        epsilon = 0.01
        delta = (1 - 2 * epsilon) / (self.individuals - 1)
        
        for i in range(self.individuals):
            lambda1 = epsilon + i * delta
            lambda2 = 1 - epsilon - i * delta
            lambdas.append((lambda1, lambda2))
        
        return lambdas
    
    def initialize_neighborhood(self):
        neighborhoods = []
        for i, lambda_i in enumerate(self.lambdas):
            neighbors = sorted(
                range(len(self.lambdas)),
                key=lambda j: math.sqrt(
                    (self.lambdas[j][0] - lambda_i[0])**2 +
                    (self.lambdas[j][1] - lambda_i[1])**2
                )
            )
            neighborhoods.append(neighbors[:self.T])
        
        return neighborhoods
        
    def _initialize_individual(self) -> tuple:
        x = np.random.uniform(self.search_space[0], self.search_space[1], self.n)
        x[0] = np.random.uniform(0, 1)  # Limit x_0 to the range (0, 1)
        return x


    # --------------- UPDATE Z VALUE ---------------

    def _update_z(self, F_y: list) -> None:
        for i in range(self.m):
            self.z[i] = min(self.z[i], F_y[i])


    # --------------- EVOLUTIONARY OPERATORS ---------------
        
    # Differencial evolution
    def _mutate(self, i: int) -> np.ndarray:
        a, b, c = np.random.choice(self.neighborhood[i], 3)
        mutated = self.population[a] + self.F * (self.population[b] - self.population[c])
        mutated[0] = np.clip(mutated[0], 0, 1) # For both functions x_0 search space is [0, 1]
        mutated[1:] = np.clip(mutated[1:], self.search_space[0], self.search_space[1])
        return mutated
    
    def _crossover(self, parent: np.ndarray, mutant: np.ndarray) -> np.ndarray:
        trial = np.copy(parent)
        i_rand = np.random.randint(len(parent))
        for i in range(self.n):
            if np.random.rand() <= self.CR:
                trial[i] = mutant[i]
        return trial

    # Gaussian mutation
    def _gaussian_mutation(self, ind: np.ndarray ) -> np.ndarray:
        sigma = (self.search_space[1] - self.search_space[0]) / 50
        for j in range(len(ind)):
            if np.random.rand() < self.MR:
                ind[j] += np.random.normal(0, sigma)
        return np.array([np.clip(x, self.search_space[0], self.search_space[1]) for x in ind])

                
    # ------------------- EVALUATION -------------------       

    def calculate_F(self, x):
        return zdt3(x) if self.function == "zdt3" else cf6(x)

    def _g_te(self, lambdas,  F_y) -> float:
        maximum_value = float("-inf")
        for j in range(self.m):
            maximum_value = max(maximum_value, lambdas[j] * abs(self.z[j] - F_y[j]))
        return maximum_value

    def calculate_constraints(self, x):
        if self.function == "zdt3":
            return constraints_zdt3(x)
        elif self.function == "cf6":
            return constraints_cf6(x)
        raise Exception("Something went wrong")


    # ------------------- MAIN LOOP -------------------       
     
    def run(self):
        acum_f = []
        for _ in range(self.iterations):
            for i in range(self.individuals):
                
                mutant = self._mutate(i)
                offspring = self._crossover(self.population[i], mutant)
                offspring = self._gaussian_mutation(offspring)
                
                f_y = self.calculate_F(offspring)
                
                trial_constraints = self.calculate_constraints(offspring)
                current_constraints = self.constraints[i]
                
                self._update_z(f_y)
                
                for j in self.neighborhood[i]:
                    g_x = self._g_te(self.lambdas[j], self.F_y[j])
                    g_y = self._g_te(self.lambdas[j], f_y)
                    
                    if trial_constraints == 0 and current_constraints == 0:
                        if g_y < g_x:
                            self.population[j] = offspring
                            self.F_y[j] = f_y
                            self.constraints[j] = trial_constraints
                    elif trial_constraints == 0 and current_constraints != 0:
                        self.population[j] = offspring
                        self.F_y[j] = f_y
                        self.constraints[j] = trial_constraints
                    elif trial_constraints != 0 and current_constraints != 0:
                        if trial_constraints < current_constraints:
                            self.population[j] = offspring
                            self.F_y[j] = f_y
                            self.constraints[j] = trial_constraints
                            
                acum_f.append((self.F_y[i], self.constraints[i]))
                
        return acum_f