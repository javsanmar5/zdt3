from algorithm.Algorithm import Algorithm
from utils.log import write_log_out
from utils.screen_plot import plot


def main() -> None:
    
    ITERATIONS = 100
    INDIVIDUALS = 40
    
    MINE_ONE="./logs/output.out"
    PROF_ONE="./data/results/prof/EVAL4000/P40G100/zdt3_all_popmp40g100_seed01.out"

    zdt3_algorithm = Algorithm(ITERATIONS, INDIVIDUALS)
    output = zdt3_algorithm.run()

    write_log_out(output)
    plot(MINE_ONE)
    plot(PROF_ONE)
    
    
if __name__ == '__main__':
    main()