def write_log_out(to_write: list, path: str) -> None:
    with open(path, "w") as file:
        for line in to_write:
            (val1, val2), val3 = line
            file.write(f"{val1:.6e}\t{val2:.6e}\t{val3:.6e}\n")
    return

def load_log_out(path: str) -> list:
    with open (path, "r") as file:
        return [[float(x) for x in line.split()] for line in file.readlines()]