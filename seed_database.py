"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())


# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    title = movie["title"]
    overview = movie["overview"]
    poster_path = movie["poster_path"]
    release_date_str = movie["release_date"]
    release_date_format = "%Y-%m-%d"
    release_date = datetime.strptime(release_date_str, release_date_format)
    

    # TODO: create a movie here and append it to movies_in_db
    movie_object = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(movie_object)

model.db.session.add_all(movies_in_db)
model.db.session.commit()

users_in_db = []
for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user_object = crud.create_user(email,password)
    users_in_db.append(user_object)

    model.db.session.add_all(users_in_db)
# model.db.session.commit()

    # TODO: create 10 ratings for the user
    for rating in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1, 5)

        rating = crud.create_rating(user_object, random_movie, score)
        model.db.session.add(rating)

model.db.session.commit()