# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    calories = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    sodium = db.Column(db.Integer)
    breakfast = db.Column(db.Boolean, default=False)
    lunch = db.Column(db.Boolean, default=False)
    dinner = db.Column(db.Boolean, default=False)
    snack = db.Column(db.Boolean, default=False)
    dessert = db.Column(db.Boolean, default=False)
