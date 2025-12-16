import json
import io
import csv
import time
from datetime import datetime


from flask import Flask, request, jsonify, Response

from src.api.models import db, CleaningSession
from src.core.robot import Robot, PremiumRobot  # Import Robot and PremiumRobot classes
from src.api.utils import parse_json_map, parse_txt_map  # Utility functions for parsing maps


app = Flask(__name__)

import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'robot_history.db')

db.init_app(app)    

current_grid = None  # Global variable to hold the current grid

@app.route('/set-map', methods=['POST'])
def set_map():
    global current_grid # Use the global variable to store the grid

    if 'file' in request.files:
        file     = request.files['file']
        filename = file.filename
        content  = file.read().decode('utf-8') # Read file content as string

        if filename.endswith('.json'):
            try: 
                data = json.loads(content)
                current_grid = parse_json_map(data)
            except json.JSONDecodeError:
                return jsonify({"error":  "Invalid JSON file"}), 400 #4XX Client Error
        elif filename.endswith('.txt'):
            try:
                # Pass raw text content to the TXT parser
                current_grid = parse_txt_map(content)
            except Exception as e:
                return jsonify({"error" : "Invalid TXT file"}), 400 #4XX Client Error
        else:
            return jsonify({"error" : "Unsupported file type"}), 400 #4XX Client Error
        
        return jsonify({"message": "Map set successfully"}), 200 #2XX Success

    return jsonify({"error" : "No file provided"}), 400 #4XX Client Error



@app.route('/clean', methods=['POST'])
def clean():
    global current_grid
    if current_grid is None:
        return jsonify({"error": "No Grid set"}), 400 #4XX Client Error

    data = request.json
    start_pos  = tuple(data.get('start_pos', (0, 0)))  # (x, y)
    commands   = data.get('commands')  # List of (direction, steps)

    model_type = request.args.get('model', 'base').lower()
    if model_type == 'premium':
        robot = PremiumRobot(grid=current_grid)
    else:
        robot = Robot(grid=current_grid)
    
    start_time = time.time()
    status, cleaned_tiles = robot.execute_commands(commands, start_pos)
    end_time   = time.time()

    duration = end_time - start_time

    # Save session to DB
    session = CleaningSession(
        start_time=datetime.fromtimestamp(start_time),
        final_state=status,
        num_actions=sum(steps for _, steps in commands),
        num_cleaned_tiles=robot.get_num_cleaned_tiles(),
        duration=duration,
    )
    db.session.add(session)
    db.session.commit()
   
    response = {
        "final_state": status,
        "cleaned_tiles": cleaned_tiles,
        "count_cleaned_tiles": robot.get_num_cleaned_tiles(),
        "model_type": model_type,
    }
    if status == "error":
        response['message'] = "Collision detected or invalid path"
    return jsonify(response), 200 #2XX Success



@app.route('/history', methods=['GET'])
def history():
    sessions = CleaningSession.query.all()

    # Generate CSV 
    output = io.StringIO() # In-memory text stream
    writer = csv.writer(output) # CSV writer object

    writer.writerow(['start_time', 'final_state', 'num_actions', 'num_cleaned_tiles', 'duration'])  # Header row  

    for session in sessions:
        writer.writerow([session.start_time, session.final_state, session.num_actions, session.num_cleaned_tiles, session.duration]) # Data rows
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=history.csv"}
    ) # Return CSV 


if __name__ == '__main__':
    app.run(debug=True, port=5000)