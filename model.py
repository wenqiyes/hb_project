"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Replace this with your code!
# multiple users can rate the same movie
# movie can have A LOT or ratings, get average score 
# 1 user can rate multiple movies 
#ratings and association withe user and movie.  Users and movies have a foreigh key 

class User(db.Model):
    """User"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

    ratings = db.relationship('Rating', back_populates = "user")

class Movie(db.Model):
    """""A movie"""""
    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)

    def __repr__(self):
        return f"<Movie movie_id={self.movie_id} title={self.title}>"

    ratings = db.relationship('Rating', back_populates = "movie")

class Rating(db.Model):
    """A movie rraating"""
    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"

    user = db.relationship('User', back_populates = "ratings")
    #ratings in 54 must match variable of ratings in 25
    movie = db.relationship('Movie', back_populates = "ratings")


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
