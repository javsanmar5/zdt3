import math

class Subproblem:
    def __init__(self, lambdas: tuple) -> None:
        self.lambdas = lambdas
        self.best_solution = None
        self.solution_fitness = None
        self.neighborhood = None
        
            
    # -------------------  SETTERS -------------------            
            
    def set_neighborhood(self, subproblems: list, T: int) -> None:
        self.neighborhood = sorted(range(len(subproblems)), key=lambda i: 
            math.sqrt((subproblems[i].lambdas[0] - self.lambdas[0])**2 + 
                    (subproblems[i].lambdas[1] - self.lambdas[1])**2))[:T]
    
    def set_best_solution(self, solution: list) -> None:
        self.best_solution = solution

    def set_solution_fitness(self, fitness: float) -> None:
        self.solution_fitness = fitness
        
    
    # ----------------- REPRESENTATION -----------------

    def __str__(self) -> str:
        return f"Subproblem(lambdas={self.lambdas}, best_solution={self.best_solution}, neighborhood={self.neighborhood})"

    def __repr__(self) -> str:
        return f"Subproblem(lambdas={self.lambdas}, best_solution={self.best_solution}, neighborhood={self.neighborhood})"