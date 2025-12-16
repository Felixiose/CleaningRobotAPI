from src.core.grid import Grid

def parse_txt_map(txt_data: str) -> Grid:
    lines = txt_data.strip().split('\n')
    rows = len(lines)
    cols = len(lines[0]) if rows > 0 else 0
    obstacles = set()
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == 'x':
                obstacles.add((x, y))
    return Grid(cols, rows, obstacles)

def parse_json_map(json_data : dict) -> Grid:
    rows = json_data.get('rows')
    cols = json_data.get('cols')
    obstacles = set()
    
    for tile in json_data.get('tiles', []):
        if not tile.get('walkable', True):
            obstacles.add((tile['x'], tile['y']))
            
    return Grid(cols, rows, obstacles)