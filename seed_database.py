"""Script to seed database."""

import os

import model
import server
from werkzeug.security import generate_password_hash

os.system('dropdb favorites')
os.system('createdb favorites')

model.connect_to_db(server.app,'favorites')
model.db.create_all()

hash_password = generate_password_hash('1234')
test_user = model.User(email='123@gmail.com', password=hash_password)
model.db.session.add(test_user)
model.db.session.commit()


# test_listing = model.Listing(name='test apartment', rating=5.0, address='test_street,test_city,test_state', zip_code=12345, phone='0001112222',image_url='https://i.picsum.photos/id/43/1280/831.jpg?hmac=glK-rQ0ppFClW-lvjk9FqEWKog07XkOxJf6Xg_cU9LI', user=test_user, yelp_id='')
# model.db.session.add(test_listing)
# model.db.session.commit()