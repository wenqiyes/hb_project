"""Script to seed database."""

import os

import model
import server

os.system('dropdb favorites')
os.system('createdb favorites')

model.connect_to_db(server.app,'favorites')
model.db.create_all()

test_user = model.User(email='123@gmail.com', password='1234')
model.db.session.add(test_user)
model.db.session.commit()


