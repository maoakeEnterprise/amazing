from parsing.Parsing import DataMaze


def main() -> None:
    print("Unit Testing for parsing:")
    data = DataMaze.get_data("config.txt")
    data_t = DataMaze.transform_data(data)
    data_t = DataMaze.verif_key_data(data_t)
    data_t = DataMaze.verif_value_data(data_t)
    print(data_t)


if __name__ == "__main__":
    main()
