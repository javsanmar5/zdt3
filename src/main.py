import random

from algorithm.Algorithm import Algorithm
from utils.log import write_log_out
from utils.screen_plot import plot

from functions.cf6_function import cf6


def main() -> None:
    
    FUNCTIONS = ["zdt3", "cf6"]
    FUNCTION = 1 # 0 -> ZDT3 | 1 -> CF6
    
    ITERATIONS = 400
    INDIVIDUALS = 10
    
    MINE_ONE="./logs/output.out"
    ZDT3_PROF_ONE="./data/results/prof/zdt3/EVAL4000/P40G100/zdt3_all_popmp40g100_seed01.out"
    CF6_PROF_ONE="./data/results/prof/cf6/EVAL4000/P40G100/cf6_4d_all_popmp40g100_seed01.out"
    OPTIMAL_PATH=["./data/zdt3_optimal_pareto.dat", "./data/cf6_optimal_pareto.dat"]

    PARAMETERS = {
        "n": 16, # Dimensions {4, 16}, by default: 4. Just works for cf6. For zdt3, it is 30
        "T": int(0.25 * 50),
        "MR": 1 / 40,           
        "SIG": 20,
        "F": 0.6,
        "CR": 0.4,
    }

    zdt3_algorithm = Algorithm(FUNCTIONS[FUNCTION], ITERATIONS, INDIVIDUALS, **PARAMETERS)
    output = zdt3_algorithm.run()
    # x = [ 0.78620844,  2.        , -0.46818091, -0.04756558]
    # cf6_ = cf6(x)
    # print(cf6_)
    # print(zdt3_algorithm._constraints(x))

    write_log_out(output)
    plot(MINE_ONE, OPTIMAL_PATH[FUNCTION])
    # plot(ZDT3_PROF_ONE, OPTIMAL_PATH[FUNCTION])
    # plot(CF6_PROF_ONE, OPTIMAL_PATH[FUNCTION])
    
    
if __name__ == '__main__':
    main()