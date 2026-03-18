from pydantic import BaseModel, Field


class Cell(BaseModel):
    value: int = Field(ge=0, le=15)

    def __str__(self) -> str:
        return hex(self.value).removeprefix("0x")

    def set_value(self, value: int) -> None:
        self.value = value

    def get_value(self) -> int:
        return self.value

    def set_north(self, is_wall: bool) -> None:
        if (not is_wall and self.value | 14 == 15) or (
            is_wall and self.value | 14 != 15
        ):
            self.value = self.value ^ (1)

    def get_north(self) -> bool:
        return self.value & 1 == 1

    def set_est(self, is_wall: bool) -> None:
        if (not is_wall and self.value | 13 == 15) or (
            is_wall and self.value | 13 != 15
        ):
            self.value = self.value ^ (2)

    def get_est(self) -> bool:
        return self.value & 2 == 2

    def set_south(self, is_wall: bool) -> None:
        if (not is_wall and self.value | 11 == 15) or (
            is_wall and self.value | 11 != 15
        ):
            self.value = self.value ^ (4)

    def get_south(self) -> bool:
        return self.value & 4 == 4

    def set_west(self, is_wall: bool) -> None:
        if (not is_wall and self.value | 8 == 15) or (
            is_wall and self.value | 8 != 15
        ):
            self.value = self.value ^ (8)

    def get_west(self) -> bool:
        return self.value & 8 == 8


def main() -> None:
    c = Cell(value=1)
    print(c.get_north())
    c.set_north(True)
    print(c.get_north())
    c.set_north(True)
    print(c.get_north())
    c.set_north(False)
    print(c.get_north())


if __name__ == "__main__":
    main()
