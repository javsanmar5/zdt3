def write_txt(to_write: list) -> None:
    with open ("./logs/output.txt", "w") as file:
        for line in to_write:
            for datum in line:
                file.write(str(datum) + " ")
            file.write("\n")
    return

def load_txt(path: str) -> list:
    with open (path, "r") as file:
        return [[float(x) for x in line.split()] for line in file.readlines()]