from ..amaz_lib import DepthFirstSearch, Kruskal
from ..amaz_lib import AStar, DepthFirstSearchSolver
from typing import Any


class DataMaze:

    @staticmethod
    def get_file_data(name_file: str) -> str:
        with open(name_file, "r") as file:
            data = file.read()
        if data == "":
            raise ValueError("The file is empty")
        return data

    @staticmethod
    def transform_data(data: str) -> dict[str, str]:
        tmp = data.split("\n")
        tmp2 = [value.split("=", 1) for value in tmp if "=" in value]
        data_t = {value[0]: value[1] for value in tmp2}
        return data_t

    @staticmethod
    def verif_key_data(data: dict[str, str]) -> None:
        key_test = {
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
            "GENERATOR",
            "SOLVER",
        }
        set_key = {key for key in data.keys()}
        if len(set_key) != len(key_test):
            raise KeyError("Missing some data the len do not correspond")
        res_key = {key for key in set_key if key not in key_test}
        if len(res_key) != 0:
            raise KeyError(
                "Some Key " f"do not correspond the keys: {res_key}"
            )

    @staticmethod
    def convert_values(data: dict[str, str]) -> dict[str, Any]:
        key_int = {"WIDTH", "HEIGHT"}
        key_tuple = {"ENTRY", "EXIT"}
        key_bool = {"PERFECT"}
        res: dict[str, Any] = {}
        for key in key_int:
            res.update({key: int(data[key])})
        for key in key_tuple:
            res.update({key: DataMaze.convert_tuple(data[key])})
        for key in key_bool:
            res.update({key: DataMaze.convert_bool(data[key])})
        res.update({"OUTPUT_FILE": data["OUTPUT_FILE"]})
        res.update(
            DataMaze.get_solver_generator(data, res["ENTRY"], res["EXIT"],
                                          res["PERFECT"])
        )
        return res

    @staticmethod
    def get_solver_generator(data: dict[str, str], entry: tuple[int, int],
                             exit: tuple[int, int],
                             perfect: bool) -> dict[str, Any]:
        available_generator: dict[str, Any] = {
            "Kruskal": Kruskal,
            "DFS": DepthFirstSearch,
        }
        available_solver: dict[str, Any] = {
            "AStar": AStar,
            "DFS": DepthFirstSearchSolver
        }
        res = {}
        res["GENERATOR"] = available_generator[data["GENERATOR"]](entry, exit,
                                                                  perfect)
        res["SOLVER"] = available_solver[data["SOLVER"]](entry, exit)
        return res

    @staticmethod
    def convert_tuple(data: str) -> tuple[int, int]:
        data_t = data.split(",")
        if len(data_t) != 2:
            raise ValueError(
                "There is too much " "argument in the coordinate given"
            )
        x, y = data_t
        tup = (int(x), int(y))
        return tup

    @staticmethod
    def convert_bool(data: str) -> bool:
        if data != "True" and data != "False":
            raise ValueError("This is not True or False")
        if data == "True":
            return True
        return False

    @staticmethod
    def get_data_maze(name_file: str) -> dict[str, Any]:
        try:
            data_str = DataMaze.get_file_data(name_file)
            data_dict = DataMaze.transform_data(data_str)
            DataMaze.verif_key_data(data_dict)
            data_maze = DataMaze.convert_values(data_dict)
            return {k.lower(): v for k, v in data_maze.items()}
        except FileNotFoundError:
            print("The file do not exist")
            exit()
        except PermissionError:
            print("We dont have the Permission")
            exit()
        except ValueError as e:
            print(f"Error during the convert or the file is empty: {e}")
            exit()
        except KeyError as e:
            print(f"Error on the key in the file: {e}")
            exit()
        except IndexError as e:
            print(
                "In the function transform Data some data cannot "
                f"be splited by '=' because '=' was not present: {e}"
            )
            exit()
        except AttributeError as e:
            print("Error on the " f"funciton get_data_maze : {e}")
            exit()
