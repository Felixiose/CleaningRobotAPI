import pytest

from src.core.grid import Grid
from src.core.robot import Robot


@pytest.fixture
def robot():
    """
    Creates a 5x5 Grid with a vertical wall at x=2.
    (0,0) (1,0) [X] (3,0) (4,0)
    ...
    """
    obstacles = {(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)}
    grid = Grid(width=5, height=5, obstacles=obstacles)
    return Robot(grid=grid)


def test_clean_path_success(robot):
    status, _ = robot.execute_commands([("south", 2)], (0, 0))
    assert status == "completed"


def test_collision_with_obstacle(robot):
    # Move East 2 steps (0,0 -> 1,0 -> 2,0[hit])
    status, _ = robot.execute_commands([("east", 3)], (0, 0))
    assert status == "error"


def test_collision_at_boundary(robot):
    # Move North from (0,0) -> outside
    status, _ = robot.execute_commands([("north", 1)], (0, 0))
    assert status == "error"


def test_invalid_starting_position(robot):
    # Start exactly on an obstacle
    status, _ = robot.execute_commands([("south", 1)], (2, 2))
    assert status == "error"


def test_stop_exactly_before_obstacle(robot):
    # Move 1 step East to (1,0). Obstacle is at (2,0). Safe.
    status, visited = robot.execute_commands([("east", 1)], (0, 0))
    assert status == "completed"
    assert (1, 0) in visited
    assert (2, 0) not in visited


def test_crash_mid_command(robot):
    # Try East 5. Should visit (0,0), (1,0) then crash at (2,0).
    status, visited = robot.execute_commands([("east", 5)], (0, 0))
    assert status == "error"
    # Logic check: Should preserve cleaned tiles before crash
    assert len(visited) == 2  # (0,0) and (1,0)
    assert (1, 0) in visited
    assert (2, 0) not in visited


def test_sequential_commands_fail_later(robot):
    # 1. South 2 (Safe) -> 2. East 3 (Crash)
    status, visited = robot.execute_commands([("south", 2), ("east", 3)], (0, 0))
    assert status == "error"
    assert (0, 2) in visited  # From first command
    assert (1, 2) in visited  # From second command before crash


def test_backtracking_unique_count(robot):
    # (0,0) -> (1,0) -> (0,0). Visited set should handle duplicates.
    status, visited = robot.execute_commands([("east", 1), ("west", 1)], (0, 0))
    assert status == "completed"
    assert len(visited) == 2  # Only unique tiles counted


def test_start_out_of_bounds_negative(robot):
    status, _ = robot.execute_commands([], (-1, -1))
    assert status == "error"


def test_start_out_of_bounds_overflow(robot):
    status, _ = robot.execute_commands([], (10, 10))
    assert status == "error"
