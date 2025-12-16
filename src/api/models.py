"""
Database Models
---------------
Defines the schema for persisting robot operation history.
Uses **SQLAlchemy ORM** to map Python classes to database tables.
"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CleaningSession(db.Model):
    """
    id (int): Unique identifier for the session.
    model_type (str): Discriminator column ('base' or 'premium').
                          Useful for analyzing performance differences between models.
    start_time (datetime): UTC timestamp of when the run began.
    final_state (str): Outcome of the run ('completed' or 'error').
    num_actions (int): Total commands executed.
    num_cleaned_tiles (int): Total unique tiles processed.
    duration (float): Execution time in seconds.
    """

    id = db.Column(db.Integer, primary_key=True)
    model_type = db.Column(db.String(20), default="base")
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    final_state = db.Column(db.String(10))
    num_actions = db.Column(db.Integer)
    num_cleaned_tiles = db.Column(db.Integer)
    duration = db.Column(db.Float)  # sec

    def to_csv_row(self) -> str:
        return f"{self.id},{self.model_type},{self.start_time},{self.final_state},{self.num_actions},{self.num_cleaned_tiles},{self.duration}\n"
