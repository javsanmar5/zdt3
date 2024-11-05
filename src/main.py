from algorithm.Algorithm import Algorithm
from utils.log import write_log_out
from utils.screen_plot import plot


def main() -> None:
    
    FUNCTIONS = ["zdt3", "cf6"]
    DIMENSIONS = 4
    function_number = 0 # 0 -> ZDT3 | 1 -> CF6

    FUNCTION = FUNCTIONS[function_number]
    OPTIMAL_PATH=["./data/zdt3_optimal_pareto.dat", "./data/cf6_optimal_pareto.dat"][function_number]
    
    ITERATIONS = 100
    INDIVIDUALS = 40

    PARAMETERS = {
        "n": DIMENSIONS, # Dimensions {4, 16}, by default: 4. Just works for cf6. For zdt3, it is 30
        "T": int(0.25 * INDIVIDUALS),
        "MR": 0.15,           
        "F": 0.7,
        "CR": 0.6,
    }

    for run in range(10):
        print(f"------------------- RUN {run} -------------------")
        if FUNCTION == "zdt3":
            MINE_ONE=f"./logs/{FUNCTION}/EVAL{ITERATIONS*INDIVIDUALS}/{FUNCTION}_P{INDIVIDUALS}G{ITERATIONS}_RUN{run}.out"
        else:
            MINE_ONE=f"./logs/{FUNCTION}_{DIMENSIONS}d/EVAL{ITERATIONS*INDIVIDUALS}/{FUNCTION}_P{INDIVIDUALS}G{ITERATIONS}_RUN{run}.out"
            
        zdt3_algorithm = Algorithm(FUNCTION, ITERATIONS, INDIVIDUALS, **PARAMETERS)
        output = zdt3_algorithm.run()

        write_log_out(to_write=output, path=MINE_ONE)
        # plot(MINE_ONE, OPTIMAL_PATH)
    
    
if __name__ == '__main__':
    main()