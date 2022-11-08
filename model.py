"""Models for Apartment Finder App"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    """User"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

    favorites = db.relationship('Favorite', back_populates = "user")
    listing = db.relationship('Listing', back_populates = "user")

    # def get_id(self):
    #     print(self.user_id)
    #     return str(self.user_id)

class Listing(db.Model):
    """An apartment listing that is added or posted by a user"""
    __tablename__ = "listings"

    listing_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String)
    rating = db.Column(db.Float)
    address = db.Column(db.String)
    zip_code=db.Column(db.Integer)
    phone = db.Column(db.String)
    image_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    yelp_id = db.Column(db.String)

    def __repr__(self):
        return f"<Listing listing_id={self.listing_id} name={self.name} zip_code={self.zip_code}>"

    favorites = db.relationship('Favorite', back_populates = "listing")
    user = db.relationship('User', back_populates = 'listing')


class Favorite(db.Model):
    """An apartment listing that is favored or posted by a user"""
    __tablename__ = "favorites"
    favorite_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    listing_id = db.Column(db.Integer,db.ForeignKey('listings.listing_id'))

    def __repr__(self):
        return f"<Favorite favorite_id={self.favorite_id} user_id={self.user_id} listing_id={self.listing_id}>"

    user = db.relationship('User', back_populates = "favorites")
    listing = db.relationship('Listing', back_populates = "favorites")

def connect_to_db(app, db_name):
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app, "favorites")

