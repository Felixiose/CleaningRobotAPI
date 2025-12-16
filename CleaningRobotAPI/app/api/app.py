import json

from utils import parse_txt_map, parse_json_map

from flask import Flask, request, jsonify
from models import db


app = Flask(__name__)
# app.config['']
db.init_app(app)    



current_grid = None  # Global variable to hold the current grid

@app.route('/set-map', methods=['POST'])
def set_map():
    global current_grid # Use the global variable to store the grid

    if 'file' in request.files:
        file     = request.files['file']
        filename = file.filename
        content = file.read().decode('utf-8') # Read file content as string

        if filename.endswith('.json'):
            try: 
                data = json.loads(content)
                current_grid = parse_json_map(data)
            except json.JSONDecodeError:
                return jsonify({"error", "Invalid JSON file"}), 400 #4XX Client Error
        elif filename.endswith('.txt'):
            try:
                data = content.splitlines()
                current_grid = parse_txt_map(data)
            except Exception as e:
                return jsonify({"error", "Invalid TXT file"}), 400 #4XX Client Error
        else:
            return jsonify({"error", "Unsupported file type"}), 400 #4XX Client Error
        
        return jsonify({"message": "Map set successfully"}), 200 #2XX Success

    return jsonify({"error", "No file provided"}), 400 #4XX Client Error



@app.route('/clean', methods=['POST'])
def clean():
    global current_grid
    if current_grid is None:
        return jsonify({"error": "No Grid set"}), 400 #4XX Client Error

    data = ...
    return 




@app.route('/history', methods=['GET'])
def history():
    return


