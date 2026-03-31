from amaz_lib.Cell import Cell


def test_cell_setter_getter() -> None:
    cell = Cell(value=0)

    cell.set_north(True)
    assert cell.get_north() is True
    cell.set_north(False)
    assert cell.get_north() is False

    cell.set_est(True)
    assert cell.get_est() is True
    cell.set_est(False)
    assert cell.get_est() is False

    cell.set_south(True)
    assert cell.get_south() is True
    cell.set_south(False)
    assert cell.get_south() is False

    cell.set_west(True)
    assert cell.get_west() is True
    cell.set_west(False)
    assert cell.get_west() is False

    cell.set_value(8)
    assert cell.get_value() == 8
    cell.set_value(0)
    assert cell.get_value() == 0
