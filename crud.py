"""CRUD operations."""

from model import db, User, Listing,Favorite, connect_to_db


# Functions start here!

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_all_users():
    """Return all users"""

    return User.query.all()

def get_user_by_id(user_id):
    """Get user details according to its id"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Get user email according to its email"""
    return User.query.filter(User.email == email).first()


def create_listing(name, rating, address, zip_code, phone,image_url, user_id, yelp_id):
    """Create and return a new listing."""

    listing = Listing(name = name, rating = rating, address = address, zip_code = zip_code, phone = phone, image_url = image_url, user_id = user_id, yelp_id = yelp_id)

    return listing

def get_all_listings():
    """"Get all the listings."""

    return Listing.query.all()

def get_listing_by_id(listing_id):
    """Get listing details according to its id"""

    return Listing.query.get(listing_id)

def get_listing_by_user_email(user_email):
    """Get Listings according to the user email"""
    user = User.query.filter(User.email == user_email).first()
    return user.listing
    

def get_listing_from_db(zip_code):
    """Get listings that is posted by the user"""
    return Listing.query.filter(Listing.zip_code == zip_code, Listing.yelp_id =='').all()

def create_favorite(user, listing):
    """Create and return a new movie."""

    favorite = Favorite(user=user, listing= listing)

    return favorite




if __name__ == '__main__':
    from server import app
    connect_to_db(app, "favorites")