"""drop and Create tables"""

from app import db
from models import User, Favorite

db.drop_all()
db.create_all()
