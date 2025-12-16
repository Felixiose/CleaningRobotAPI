"""
Grid Domain Logic
-----------------
Defines the spatial environment for the robot
"""

from abc import ABC, abstractmethod


class GridBase(ABC):
    """
    Abstract Interface for Grid implementations.
    Enforces that any grid must provide a validity check for coordinates.
    """

    @abstractmethod
    def is_valid_move(self, position: tuple[int, int]) -> bool:
        pass


class Grid(GridBase):
    """
    Standard Rectangular Grid Implementation.

    Attributes:
        width (int): The X-axis limit (exclusive).
        height (int): The Y-axis limit (exclusive).
        obstacles (set): A hashed set of coordinate tuples for O(1) lookup performance.
    """

    def __init__(self, width: int, height: int, obstacles: set[tuple[int, int]]):
        self.width = width
        self.height = height
        self.obstacles = obstacles  # Set of (x, y) tuples representing obstacles

    def is_valid_move(self, position: tuple[int, int]) -> bool:
        """
        Takes position (tuple): (x, y) coordinates.
        Returns True if the space is walkable, False if blocked or out-of-bounds.
        """
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
