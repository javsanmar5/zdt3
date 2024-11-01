import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from utils.log import load_log_out


def plot(filepath: str, optimal_path: str) -> None:
    
    data = load_log_out(path=filepath)
    optimal = load_log_out(path=optimal_path)

    f1_values = [row[0] for row in data]
    f2_values = [row[1] for row in data]
    restrictions = [row[2] for row in data]  

    f1_optimal = [row[0] for row in optimal]
    f2_optimal = [row[1] for row in optimal]

    restricted_indices = [i for i, r in enumerate(restrictions) if r != 0]
    unrestricted_indices = [i for i, r in enumerate(restrictions) if r == 0]

    num_points = len(unrestricted_indices)
    colors = np.linspace(0, 1, num_points)

    plt.figure(figsize=(10, 8))

    scatter = plt.scatter(
        [f1_values[i] for i in unrestricted_indices],
        [f2_values[i] for i in unrestricted_indices],
        c=colors, cmap='coolwarm', label='Data'
    )

    plt.scatter(
        [f1_values[i] for i in restricted_indices],
        [f2_values[i] for i in restricted_indices],
        color='black', label='With Restriction'
    )

    plt.scatter(f1_optimal, f2_optimal, color='green', label='Optimal')

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Data'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8, label='Optimal'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='With Restriction')
    ]
    
    plt.xlabel('f1(x)')
    plt.ylabel('f2(x)')
    plt.title('Scatter plot of f1(x) vs f2(x)')
    plt.colorbar(scatter, label='Progression through file')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-1, 3)
    plt.grid(True)
    plt.legend(handles=legend_elements)
    plt.show()