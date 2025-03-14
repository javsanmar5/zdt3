# Multi-Objective Optimization Solver

## Description
`multiobjective-optimization` is a Python project that solves multi-objective optimization problems using an evolutionary algorithm. The project currently supports:
- **ZDT3**: A well-known benchmark problem for multi-objective optimization.
- **CF6**: Another complex multi-objective optimization problem, implemented for different dimensions.

It should works with any problem but is tested and done with the aim of solving these two. The projects implements:

- Implements an evolutionary algorithm to solve multi-objective problems.
- Supports multiple test functions (ZDT3 and CF6).
- Includes mutation and neighborhood update mechanisms.
- Tracks and updates the best solutions found during the iterations.

## Installation
To install and run this project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/javsanmar5/multiobjective-optimization.git
    cd multiobjective-optimization
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
To run the algorithm, execute the following command:
```sh
python ./src/main.py
```
To run the metric software:
```sh
cd bin
./metrics
Follow the instructions
```

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Authors
- Javier Santos (https://github.com/javsanmar5)

