class DataMaze:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_data(name_file: str) -> str:
        data = ""
        try:
            with open(name_file, "r") as file:
                data = file.read()
        except FileNotFoundError:
            print("The file do not exist")
        finally:
            return data

    @staticmethod
    def transform_data(data: str):
        pass
