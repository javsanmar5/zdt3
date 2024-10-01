from algorithm.Algorithm import Algorithm
from utils.log import write_txt
from utils.screen_plot import plot


def main() -> None:
    
    ITERATIONS = 150
    INDIVIDUALS = 80

    zdt3_algorithm = Algorithm(ITERATIONS, INDIVIDUALS)
    output = zdt3_algorithm.run()
    
    write_txt(output)
    plot()
    
    
    
if __name__ == '__main__':
    main()