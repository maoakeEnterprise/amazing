class DataMaze:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_data(name_file: str):
        try:
            with open(name_file, "r") as file:
                print(file)
        except FileNotFoundError:
            print("The file do not exist")
