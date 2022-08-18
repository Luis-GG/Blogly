"""Seed file to make sample data for blogly db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
user1 = User(first_name='Luis', last_name='Garcia')
user2 = User(first_name='Shayla', last_name='Holbrook')
user3 = User(first_name='Janis', last_name='Podolak')

# Add new object)
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Commit--otherwise, this never gets saved!
db.session.commit()
