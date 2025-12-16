import pytest, io
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.api.app import app, db, CleaningSession
import src.api.app as app_module

@pytest.fixture
def client():
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.test_client() as c:
        with app.app_context():
            db.drop_all(); db.create_all()
            app_module.current_grid = None
        yield c

def test_set_map_no_file(client):
    res = client.post('/set-map')
    assert res.status_code == 400 and b"No file provided" in res.data

@patch("src.api.app.parse_json_map")
def test_set_map_valid_json(mock_parser, client):
    data = {'file': (io.BytesIO(b'{"tiles": []}'), 'map.json')}
    res = client.post('/set-map', data=data, content_type='multipart/form-data')
    assert res.status_code == 200 and mock_parser.called

def test_clean_no_grid_set(client):
    res = client.post('/clean', json={'start_pos': [0,0], 'commands': []})
    assert res.status_code == 400 and b"No Grid set" in res.data

@patch("src.api.app.Robot")
@patch("src.api.app.parse_json_map")
def test_clean_success(mock_parser, MockRobot, client):
    client.post('/set-map', data={'file': (io.BytesIO(b'{}'), 'map.json')})
    
    bot = MockRobot.return_value
    bot.execute_commands.return_value = ("completed", [(0,0), (0,1)])
    bot.get_num_cleaned_tiles.return_value = 5

    res = client.post('/clean', json={"start_pos": [0, 0], "commands": [["north", 1]]})
    assert res.status_code == 200
    assert res.json['final_state'] == "completed" and res.json['count_cleaned_tiles'] == 5

def test_history_csv(client):
    with app.app_context():
        db.session.add(CleaningSession(
            start_time=datetime(2025, 12, 15), final_state="completed",
            num_actions=10, num_cleaned_tiles=5, duration=2.5
        ))
        db.session.commit()

    res = client.get('/history')
    assert "text/csv" in res.headers["Content-Type"]
    assert "completed,10,5,2.5" in res.data.decode()