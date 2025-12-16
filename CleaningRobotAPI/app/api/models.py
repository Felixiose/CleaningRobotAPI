from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() # Initialize SQLAlchemy instance for database 

class CleaningSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time  = db.Column(db.DateTime, default=datetime.utcnow)
    final_state = db.Column(...) 
    num_actions = db.Column(db.Integer)
    num_cleaned_tiles = db.Column(db.Integer)
    duration = db.Column(db.Float) # in seconds

    def to_csv_row(self) -> str:
        return f"{self.id},{self.start_time},{self.final_state},{self.num_actions},{self.num_cleaned_tiles},{self.duration}\n"
    

    