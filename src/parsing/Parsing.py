from src.amaz_lib.MazeGenerator import DepthFirstSearch, Kruskal
from src.amaz_lib.MazeSolver import AStar, DepthFirstSearchSolver


class DataMaze:
    """Provide helper methods to load and validate maze configuration data."""

    @staticmethod
    def get_file_data(name_file: str) -> str:
        """Read and return the contents of a configuration file.

        Args:
            name_file: Path to the configuration file.

        Returns:
            The file contents as a string.

        Raises:
            ValueError: If the file is empty.
        """
        with open(name_file, "r") as file:
            data = file.read()
        if data == "":
            raise ValueError("The file is empty")
        return data

    @staticmethod
    def transform_data(data: str) -> dict:
        """Transform raw configuration text into a dictionary.

        Each non-empty line containing ``=`` is split into a key-value pair.

        Args:
            data: Raw configuration text.

        Returns:
            A dictionary mapping configuration keys to their string values.
        """
        tmp = data.split("\n")
        tmp2 = [value.split("=", 1) for value in tmp if "=" in value]
        data_t = {value[0]: value[1] for value in tmp2}
        return data_t

    @staticmethod
    def verif_key_data(data: dict) -> None:
        """Validate that the configuration contains the expected keys.

        Args:
            data: Configuration dictionary to validate.

        Raises:
            KeyError: If keys are missing or unexpected keys are present.
        """
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
    def convert_values(data: dict):
        """Convert configuration values to their appropriate Python types.

        Args:
            data: Raw configuration dictionary with string values.

        Returns:
            A dictionary containing converted values and instantiated solver and
            generator objects.
        """
        key_int = {"WIDTH", "HEIGHT"}
        key_tuple = {"ENTRY", "EXIT"}
        key_bool = {"PERFECT"}
        res: dict = {}
        for key in key_int:
            res.update({key: int(data[key])})
        for key in key_tuple:
            res.update({key: DataMaze.convert_tuple(data[key])})
        for key in key_bool:
            res.update({key: DataMaze.convert_bool(data[key])})
        res.update({"OUTPUT_FILE": data["OUTPUT_FILE"]})
        res.update(
            DataMaze.get_solver_generator(
                data,
                res["ENTRY"],
                res["EXIT"],
                res["PERFECT"],
            )
        )
        return res

    @staticmethod
    def get_solver_generator(
        data: dict,
        entry: tuple,
        exit: tuple,
        perfect: bool,
    ) -> dict:
        """Instantiate the configured maze generator and solver.

        Args:
            data: Raw configuration dictionary.
            entry: Entry coordinates.
            exit: Exit coordinates.
            perfect: Whether the maze must be perfect.

        Returns:
            A dictionary containing initialized ``GENERATOR`` and ``SOLVER``
            objects.
        """
        available_generator = {
            "Kruskal": Kruskal,
            "DFS": DepthFirstSearch,
        }
        available_solver = {"AStar": AStar, "DFS": DepthFirstSearchSolver}
        res = {}
        res["GENERATOR"] = available_generator[data["GENERATOR"]](
            entry,
            exit,
            perfect,
        )
        res["SOLVER"] = available_solver[data["SOLVER"]](entry, exit)
        return res

    @staticmethod
    def convert_tuple(data: str) -> tuple:
        """Convert a comma-separated coordinate string into a tuple.

        Args:
            data: Coordinate string in the form ``"x,y"``.

        Returns:
            A tuple of two integers.

        Raises:
            ValueError: If the coordinate string does not contain exactly two
                values.
        """
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
        """Convert a string to a boolean value.

        Args:
            data: String representation of a boolean.

        Returns:
            ``True`` if the string is ``"True"``, otherwise ``False``.

        Raises:
            ValueError: If the string is neither ``"True"`` nor ``"False"``.
        """
        if data != "True" and data != "False":
            raise ValueError("This is not True or False")
        if data == "True":
            return True
        return False

    @staticmethod
    def get_data_maze(name_file: str) -> dict:
        """Load, validate, and convert maze configuration data from a file.

        Args:
            name_file: Path to the configuration file.

        Returns:
            A dictionary of validated configuration values with lowercase keys.
        """
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
