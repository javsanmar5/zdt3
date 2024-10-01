import matplotlib.pyplot as plt

from utils.log import load_txt


def plot() -> None:
    data = load_txt(path="./logs/output.txt")

    f1_values = [row[0] for row in data]
    f2_values = [row[1] for row in data]

    plt.figure(figsize=(8, 6))
    plt.scatter(f1_values, f2_values, color='blue')

    plt.xlabel('f1(x)')
    plt.ylabel('f2(x)')
    plt.title('Scatter plot of f1(x) vs f2(x)')

    plt.grid(True)
    plt.show()

