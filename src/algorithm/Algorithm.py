import random

import numpy as np

from algorithm.Subproblem import *
from functions.cf6_function import cf6
from functions.zdt3_function import zdt3


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
        self.SIG = kwargs.get("SIG", 20)
        self.F = kwargs.get("F", 0.5)
        self.CR = kwargs.get("CR", 0.5)
        self.PR = kwargs.get("PR", 1 / self.n)
        
        # INITIALIZE POPULATION
        self.population = [self._initialize_individual() for _ in range(self.individuals)]
        self.z = [min(pair[1][i] for pair in self.population) for i in range(self.m)]
        self.subproblems = self._initialize_subproblems()
        

    # -------------- AUXILIAR INITIALIZATION --------------

    def _initialize_individual(self) -> tuple:
        x = np.random.uniform(self.search_space[0], self.search_space[1], self.n)
        x[0] = np.random.uniform(0, 1)  # Limit x_0 to the range (0, 1)
        return x, Algorithm.F(x, self.function), self._constraints(x)

    def _initialize_subproblems(self) -> list[Subproblem]:
        subproblems = []
        epsilon = 0.01
        delta = (1 - 2 * epsilon) / (self.individuals - 1)
        
        for i in range(self.individuals):
            lambda1 = epsilon + i * delta
            lambda2 = 1 - epsilon - i * delta
            subproblems.append(Subproblem(lambdas=(lambda1, lambda2)))
        
        self._set_data_to_subproblems(subproblems)

        return subproblems
    
    def _set_data_to_subproblems(self, subproblems) -> None:
        for i in range(len(subproblems)):
            subproblem = subproblems[i]
            subproblem.set_neighborhood(subproblems, self.T)
            subproblem.set_best_solution(self.population[i])
            subproblem.set_solution_fitness(self._g_te(lambdas= subproblem.lambdas ,F_y= subproblem.best_solution[1]))
        
    
    def _update_z(self, F_y: list) -> None:
        for i in range(self.m):
            self.z[i] = min(self.z[i], F_y[i])
            
    

    # --------------- EVOLUTIONARY OPERATORS ---------------
    
    # Abstraction layer
    def generate_new_individual(self, i: int) -> np.ndarray[np.float64]:

        to_return = self.population[i]

        # Differential evolution
        mutant = self._mutate(i)  
        trial = self._crossover(self.population[i][0], mutant)  
        
        # Gaussian mutation
        # trial = self._gaussian_mutation(trial)
        
        trial_F_y = Algorithm.F(trial, self.function)
        trial_g_te = self._g_te(lambdas= self.subproblems[i].lambdas, F_y=trial_F_y)
        trial_constraints = self._constraints(trial)
        trial_individual = trial, trial_F_y, trial_constraints
        
        current_g_te = self._g_te(lambdas= self.subproblems[i].lambdas, F_y=to_return[1])
        current_constraints = self.population[i][2]
        
        # Choose the next individual
        
        if trial_constraints == 0 and current_constraints == 0:
            if trial_g_te < current_g_te:
                to_return = trial_individual
        elif trial_constraints == 0 and current_constraints != 0:
            to_return = trial_individual
        elif trial_constraints != 0 and current_constraints !=0:
            if trial_constraints < current_constraints:
                to_return = trial_individual
                
        return to_return
        
        
    # Differencial evolution
    def _mutate(self, i: int) -> np.ndarray:
        a, b, c = random.sample(self.subproblems[i].neighborhood, 3)
        mutated = self.population[a][0] + self.F * (self.population[b][0] - self.population[c][0])
        mutated[0] = np.clip(mutated[0], 0, 1) # For both functions x_0 search space is [0, 1]
        mutated[1:] = np.clip(mutated[1:], self.search_space[0], self.search_space[1])
        return mutated
    
    def _crossover(self, parent: np.ndarray, mutant: np.ndarray) -> np.ndarray:
        trial = np.copy(parent)
        for i in range(self.n):
            if random.random() < self.CR:
                trial[i] = mutant[i]
        return trial
    
    
    # Something else (?)
    def _gaussian_mutation(self, individual: np.ndarray) -> np.ndarray:
        trial = individual.copy()
        for j in range(len(trial)):
            if random.random() < self.PR:
                trial[j] += np.random.normal(0, self.SIG)
                if j == 0:
                    trial[j] = np.clip(trial[j], 0, 1) # For both functions x_0 search space is [0, 1]
                else:
                    trial[j] = np.clip(trial[j], self.search_space[0], self.search_space[1])
        return trial

                
    # ------------------- EVALUATION -------------------       

    @staticmethod
    def F(x, function: str):
        return zdt3(x) if function == "zdt3" else cf6(x)

    def _g_te(self, lambdas,  F_y) -> float:
        maximum_value = float("-inf")
        for j in range(self.m):
            maximum_value = max(maximum_value, lambdas[j] * abs(self.z[j] - F_y[j]))
        return maximum_value
    

    def _constraints(self, x):
        if self.function == "zdt3":
            return 0
        return self._constraint1(x) + self._constraint2(x)
        
    def _constraint1(self, x):
        left_term = x[1] - 0.8 * x[0] * np.sin(6 * np.pi * x[0] + (2 * np.pi / self.n))
        term = 0.5 * (1 - x[0]) - (1 - x[0]) ** 2
        right_term = np.sign(term) * np.sqrt(abs(term))
        if left_term - right_term < 0:
            return left_term - right_term
        return 0
    
    def _constraint2(self, x):
        left_term = x[3] - 0.8 * x[0] * np.sin(6 * np.pi * x[0] + (4 * np.pi / self.n))
        term = 0.25 * np.sqrt(1 - x[0]) - 0.5 * (1 - x[0])
        right_term = np.sign(term) * np.sqrt(abs(term))
        if left_term - right_term < 0:
            return left_term - right_term
        return 0
        
    # ------------------- MAIN LOOP -------------------       
     
    def run(self):
        acum_f = []
        for _ in range(self.iterations):
            next_population = [_ for _ in range(self.individuals)]
            for i in range(self.individuals):

                y = self.generate_new_individual(i)
                next_population[i] = y
                
                self._update_z(next_population[i][1])
                
                for subproblem in self.subproblems[i].neighborhood:
                    current_g_te= self._g_te(lambdas= self.subproblems[subproblem].lambdas, F_y=next_population[i][1])
                    if current_g_te < self.subproblems[subproblem].solution_fitness:
                        self.subproblems[subproblem].set_best_solution(y)
                        self.subproblems[subproblem].set_solution_fitness(current_g_te)

                # if _ == self.individuals -1: acum_f.append((next_population[i][1], next_population[i][2]))
                acum_f.append((next_population[i][1], next_population[i][2]))

                
            self.population = next_population

        return acum_f