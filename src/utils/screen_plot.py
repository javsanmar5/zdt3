import matplotlib.pyplot as plt
import numpy as np

from utils.log import load_log_out

# def plot() -> None:
#     data = load_txt(path="./logs/output.txt")

#     f1_values = [row[0] for row in data]
#     f2_values = [row[1] for row in data]

#     plt.figure(figsize=(8, 6))
#     plt.scatter(f1_values, f2_values, color='blue')

#     plt.xlabel('f1(x)')
#     plt.ylabel('f2(x)')
#     plt.title('Scatter plot of f1(x) vs f2(x)')

#     plt.grid(True)
#     plt.show()


# -------------------  COLOR CHANGES -------------------

def plot(filepath: str) -> None:
    data = load_log_out(path=filepath)

    f1_values = [row[0] for row in data]
    f2_values = [row[1] for row in data]

    num_points = len(f1_values)
    colors = np.linspace(0, 1, num_points)  

    plt.figure(figsize=(8, 6))

    plt.scatter(f1_values, f2_values, c=colors, cmap='coolwarm')

    plt.xlabel('f1(x)')
    plt.ylabel('f2(x)')
    plt.title('Scatter plot of f1(x) vs f2(x)')

    plt.colorbar(label='Progression through file')      
    plt.grid(True)
    plt.show()
