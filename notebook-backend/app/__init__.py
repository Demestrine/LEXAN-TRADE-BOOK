# app/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# IMPORT MODELS HERE - This is needed for Flask-Migrate to detect them
from app.models import Folder, Image

