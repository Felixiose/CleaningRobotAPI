from abc import ABC, abstractmethod
from app.core.grid import Grid


class RobotBase(ABC):

    def __init__(self, grid : Grid):
        self.grid = grid
        self.position = (0, 0)  # Starting position
        self.cleaned_tiles = set()

    def move(self, dir: str) -> bool:
        if dir == "north":
            new_position = (self.position[0], self.position[1] - 1)
        elif dir == "south":
            new_position = (self.position[0], self.position[1] + 1)
        elif dir == "east":
            new_position = (self.position[0] + 1, self.position[1])
        elif dir == "west":
            new_position = (self.position[0] - 1, self.position[1])
        else:
            raise ValueError("Invalid direction")
        if self.grid.is_valid_move(new_position):
            self.position = new_position
            return True
        return False

    def execute_commands(self, commands: list[tuple[str, int]], starting_pos: tuple[int, int]) -> str:
        # Check that format is correct
        self.position = starting_pos
        for direction, steps in commands: 
            for _ in range(steps):
                success = self.move(direction)
                if not success:
                    return "error", list(self.cleaned_tiles)
                self.cleaned_tiles.add(self.position)
        return "completed", list(self.cleaned_tiles)
               
    def get_num_cleaned_tiles(self) -> int:
        return len(self.cleaned_tiles)
            
    def reset_position(self) -> None:
        self.position = (0, 0)

    # @abstractmethod
    # def detect_dirty(self) -> bool:
    #     pass
            

class Robot(RobotBase):
    def __init__(self, grid: Grid):
        super().__init__(grid)

 

