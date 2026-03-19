class DataMaze:

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
    def transform_data(data: str) -> dict:
        tmp = data.split("\n")
        tmp2 = [
            value.split("=", 1) for value in tmp
        ]
        data_t = {
            value[0]: value[1] for value in tmp2
        }
        return data_t

    @staticmethod
    def verif_key_data(data: dict) -> dict:
        key_test = {
            "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
        }
        set_key = {
            key for key in data.keys()
        }
        try:
            res_key = {}
            if len(set_key) != len(key_test):
                raise Exception("Missing some data the len do not correspond")
            res_key = {key for key in set_key if key not in key_test}
            if len(res_key) != 0:
                raise Exception("Some Key "
                                f"do not correspond the keys: {res_key}")
            return data
        except Exception as e:
            print(f"{e}")
            exit()

    @staticmethod
    def verif_value_data(data: dict):
        key_int = {"WIDTH", "HEIGHT"}
        key_tuple = {"ENTRY", "EXIT"}
        key_bool = {"PERFECT"}
        try:
            res: dict = {}
            for key in key_int:
                res.update({key: int(data[key])})
            for key in key_tuple:
                res.update({key: DataMaze.convert_tuple(data[key])})
            for key in key_bool:
                res.update({key: DataMaze.convert_bool(data[key])})
            return res
        except ValueError as e:
            print("Error on the method verif_value_data"
                  f" in the class DataMaze: {e}")

    @staticmethod
    def convert_tuple(data: str) -> tuple:
        try:
            data_t = data.split(",")
            x, y = data_t
            tup = (int(x), int(y))
            return tup
        except ValueError as e:
            print(f"On the convert Tuple: {e}")
            exit()

    @staticmethod
    def convert_bool(data: str) -> bool:
        try:
            if data != "True" and data != "False":
                raise ValueError("This is not True or False")
            if data == "True":
                return True
            return False
        except ValueError as e:
            print(f"Error on the convert_bool in class DataMaze: {e}")
            exit()
