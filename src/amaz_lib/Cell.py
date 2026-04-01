from dataclasses import dataclass


@dataclass
class Cell:
    """Represent a maze cell encoded as a bitmask of surrounding walls.

    The cell value is stored as an integer where each bit represents the
    presence of a wall in one cardinal direction:

    - bit 0 (1): north wall
    - bit 1 (2): east wall
    - bit 2 (4): south wall
    - bit 3 (8): west wall
    """

    def __init__(self, value: int) -> None:
        """Initialize a cell with its encoded wall value.

        Args:
            value: Integer bitmask representing the cell walls.
        """
        self.value = value

    def __str__(self) -> str:
        """Return the hexadecimal representation of the cell value.

        Returns:
            The uppercase hexadecimal form of the cell value without the
            ``0x`` prefix.
        """
        return hex(self.value).removeprefix("0x").upper()

    def set_value(self, value: int) -> None:
        """Set the encoded value of the cell.

        Args:
            value: Integer bitmask representing the cell walls.
        """
        self.value = value

    def get_value(self) -> int:
        """Return the encoded value of the cell.

        Returns:
            The integer bitmask representing the cell walls.
        """
        return self.value

    def set_north(self, is_wall: bool) -> None:
        """Set or clear the north wall.

        Args:
            is_wall: ``True`` to add the north wall, ``False`` to remove it.
        """
        if (not is_wall and self.value | 14 == 15) or (
            is_wall and self.value | 14 != 15
        ):
            self.value = self.value ^ (1)

    def get_north(self) -> bool:
        """Return whether the north wall is present.

        Returns:
            ``True`` if the north wall is set, otherwise ``False``.
        """
        return self.value & 1 == 1

    def set_est(self, is_wall: bool) -> None:
        """Set or clear the east wall.

        Args:
            is_wall: ``True`` to add the east wall, ``False`` to remove it.
        """
        if (not is_wall and self.value | 13 == 15) or (
            is_wall and self.value | 13 != 15
        ):
            self.value = self.value ^ (2)

    def get_est(self) -> bool:
        """Return whether the east wall is present.

        Returns:
            ``True`` if the east wall is set, otherwise ``False``.
        """
        return self.value & 2 == 2

    def set_south(self, is_wall: bool) -> None:
        """Set or clear the south wall.

        Args:
            is_wall: ``True`` to add the south wall, ``False`` to remove it.
        """
        if (not is_wall and self.value | 11 == 15) or (
            is_wall and self.value | 11 != 15
        ):
            self.value = self.value ^ (4)

    def get_south(self) -> bool:
        """Return whether the south wall is present.

        Returns:
            ``True`` if the south wall is set, otherwise ``False``.
        """
        return self.value & 4 == 4

    def set_west(self, is_wall: bool) -> None:
        """Set or clear the west wall.

        Args:
            is_wall: ``True`` to add the west wall, ``False`` to remove it.
        """
        if (not is_wall and self.value | 7 == 15) or (
            is_wall and self.value | 7 != 15
        ):
            self.value = self.value ^ (8)

    def get_west(self) -> bool:
        """Return whether the west wall is present.

        Returns:
            ``True`` if the west wall is set, otherwise ``False``.
        """
        return self.value & 8 == 8
