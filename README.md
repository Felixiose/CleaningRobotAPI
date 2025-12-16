### CleaningRobotAPI

REST API to control and simulate a cleaning robot on a 2D grid.  
You can upload a map, run cleaning sessions with different robot models, and export execution history as CSV.

---

### Prerequisites

- **Python**: 3.12+ 
- **uv**: environment manager  
  - Install via `pip install uv` or `brew install uv`

---

### Setup & Installation

- **Install dependencies and create the virtual environment**:

```bash
uv sync
```

This will:
- create a `.venv` for the project
- install all runtime and dev dependencies (Flask, SQLAlchemy, pytest, etc.)

---

### Running the API

From the project root:

```bash
uv run python -m src.api.app
```

By default the server starts at: `http://127.0.0.1:5000`

The SQLite database file is created next to the API module (e.g. `src/api/robot_history.db`).

---

### Running Tests

The project uses **pytest** and is configured in `pyproject.toml`.

- **Run the full test suite**:

```bash
uv run python -m pytest
```

---

### API Reference

- **1. Set Environment Map**

  - **Endpoint**: `POST /set-map`
  - **Body**:  (`.txt` or `.json`)

  ```bash
  curl -F "file=@examples/map.txt" http://127.0.0.1:5000/set-map
  ```

- **2. Execute Cleaning Session (Base Model)**

  Runs the standard robot over the currently loaded grid.

  - **Endpoint**: `POST /clean`
  - **Body (JSON)**:
    - `start_pos`: `[x, y]`
    - `commands`: `[[direction, steps], ...]` where directions are `"north"`, `"south"`, `"east"`, `"west"`

  ```bash
  curl -H "Content-Type: application/json" \
       -d '{"start_pos":[0,0],"commands":[["east",2]]}' \
       http://127.0.0.1:5000/clean
  ```
  This will produce an error status as we're doing illegal moves.

- **3. Execute Cleaning Session (Premium Model)**

  Uses a `PremiumRobot` (enhanced behavior, e.g. dirt sensors).  
  The only difference at the API level is a query parameter.

  - **Endpoint**: `POST /clean?model=premium`

  ```bash
  curl -H "Content-Type: application/json" \
       -d '{"start_pos":[0,0],"commands":[["east",5]]}' \
       "http://127.0.0.1:5000/clean?model=premium"
  ```
  This might produce an error or not. It is not deterministic as no dirt sensor really exists on the robot.

Format of Respone:
```
{
  "cleaned_tiles": list[tuple[int, int]]]
  "count_cleaned_tiles": int,
  "final_state": "error" or "completed",
  "message": str,
  "model_type": "premium" or "base"
}
```
- **4. Download Cleaning History**

  Returns all past sessions as a CSV file.

  - **Endpoint**: `GET /history`

  ```bash
  curl -OJ http://127.0.0.1:5000/history
  ```

---

### Grid Formats

- **Text file (`.txt`)**

  Simple grid where:
  - `o` = walkable tile
  - `x` = obstacle

  ```txt
  ooxoo
  ooxoo
  ooooo
  ```

- **JSON file (`.json`)**

  Explicit grid size and list of tiles with walkability flags:

  ```json
  {
    "rows": 10,
    "cols": 10,
    "tiles": [
      { "x": 2, "y": 0, "walkable": false }
    ]
  }
  ```

---

### Project Structure (High Level)

- **`src/core`**: core simulation logic (`Grid`, `Robot`, etc.)
- **`src/api`**: Flask app, models, and map-parsing utilities
- **`tests`**: pytest-based unit tests for core logic and REST API


