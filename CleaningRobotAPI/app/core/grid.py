from abc import ABC, abstractmethod

class GridBase(ABC):    
    @abstractmethod
    def is_valid_move(self, position: tuple[int, int]) -> bool:
        pass

class Grid(GridBase):
    def __init__(self, width: int, height: int, obstacles: set[tuple[int, int]]):
        self.width = width
        self.height = height
        self.obstacles = obstacles # Set of (x, y) tuples representing obstacles

    def is_valid_move(self, position: tuple[int, int]) -> bool:
        x, y = position
        # check if within bounds
        if not (0 <= x < self.width):
             return False
        if not (0 <= y < self.height):
            return False
        # check if not an obstacle
        if position in self.obstacles:
            return False
        # all checks passed
        return True


