from CleaningRobotAPI.app.core.grid import Grid
from CleaningRobotAPI.app.core.robot import Robot

import unittest


class TestRobotCollision(unittest.TestCase):

    def setUp(self):
        """
        Creates a 5x5 Grid with a wall of obstacles in the middle.
        
        o o x o o
        o o x o o
        o o x o o
        o o x o o  
        o o x o o

        'o' = free space
        'x' = obstacle
        """
        obstacles = {(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)}
        self.grid = Grid(width=5, height=5, obstacles=obstacles)
        self.robot = Robot(grid=self.grid)
     
    def test_clean_path_success(self):
        """Test a valid path that does not hit walls."""
        # Move South 2 steps from (0,0) -> (0,2)
        self.robot.reset_position()
        commands = ["south", "south"]
        status  = self.robot.execute_commands(commands)
        self.assertEqual(status, "completed")

    def test_collision_with_obstacle(self):
        """Test a path that attempts to move through an obstacle."""
        # Move East 2 steps from (0,0) -> (2,0) which is blocked by an obstacle
        self.robot.reset_position()
        commands = ["east", "east", "east"]
        status  = self.robot.execute_commands(commands)
        self.assertEqual(status, "error")

    def test_collision_at_boundary(self):
        """Test a path that attempts to move outside the grid boundaries."""
        self.robot.reset_position()
        commands = ["west"]
        status = self.robot.execute_commands(commands)
        self.assertEqual(status, "error")


if __name__ == "__main__":
    unittest.main()