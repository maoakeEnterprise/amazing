from parsing.Parsing import DataMaze
import pytest


class TestParsing:

    def test_get_data_valid(self):
        data = DataMaze.get_file_data("tests/test_txt/config_1.txt")
        assert isinstance(data, str) is True

    def test_file_error(self):
        with pytest.raises(FileNotFoundError):
            DataMaze.get_file_data("tete")

    def test_permission_error(self):
        with pytest.raises(PermissionError):
            DataMaze.get_file_data("tests/test_txt/error_1.txt")

    def test_empty_file_error(self):
        with pytest.raises(ValueError):
            DataMaze.get_file_data("tests/test_txt/error_6.txt")

    def test_transform_data_valid(self):
        data = DataMaze.get_file_data("tests/test_txt/config_1.txt")
        data_2 = DataMaze.transform_data(data)
        assert isinstance(data_2, dict)

    def test_transform__index_error(self):
        with pytest.raises(IndexError):
            DataMaze.transform_data("asdasdasdasdasdasda\nasdasdas=asdasd")

    def test_key_data_error(self):
        with pytest.raises(KeyError):
            data = DataMaze.get_file_data("tests/test_txt/error_8.txt")
            data2 = DataMaze.transform_data(data)
            DataMaze.verif_key_data(data2)

    def test_key_data_error_2(self):
        with pytest.raises(KeyError):
            data = DataMaze.get_file_data("tests/test_txt/error_9.txt")
            data2 = DataMaze.transform_data(data)
            DataMaze.verif_key_data(data2)

    def test_convert_int(self):
        with pytest.raises(ValueError):
            data = DataMaze.get_file_data("tests/test_txt/error_2.txt")
            data2 = DataMaze.transform_data(data)
            DataMaze.convert_values(data2)

    def test_tuple_error(self):
        with pytest.raises(ValueError):
            DataMaze.convert_tuple("0,3,5,5")

    def test_tuple_error1(self):
        with pytest.raises(AttributeError):
            DataMaze.convert_tuple(None)

    def test_bool_error(self):
        with pytest.raises(ValueError):
            DataMaze.convert_bool("Trueeee")

    def test_valid_tuple(self):
        assert DataMaze.convert_tuple("7534564654, 78") == (7534564654, 78)

    def test_valid_bool(self):
        assert DataMaze.convert_bool("False") is False

    def test_valid_bool1(self):
        assert DataMaze.convert_bool("True") is True
