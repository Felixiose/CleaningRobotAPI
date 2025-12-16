from abc import ABC, abstractmethod
from CleaningRobotAPI.app.core.grid import Grid


class RobotBase(ABC):

    def __init__(self, grid : Grid):
        self.grid = grid
        self.position = (0, 0)  # Starting position

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
    
    def execute_commands(self, commands: list[str]) -> None:
        for command in commands:
            success = self.move(command)
            if not success:
                return "error"
        return "completed"
            
    def reset_position(self) -> None:
        self.position = (0, 0)
            

class Robot(RobotBase):
    def __init__(self, grid: Grid):
        super().__init__(grid)
    

