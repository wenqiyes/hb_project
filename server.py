"""Server for movie ratings app."""

from pprint import pformat

from flask import Flask, render_template, request, flash, session, redirect,url_for
from model import connect_to_db, db, User, Listing, Favorite
import requests
import json
import os
import crud
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import werkzeug.security


from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return crud.get_user_by_id(int(user_id))

class RegisterForm(FlaskForm):
    email = StringField(validators=[
                           InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, email):
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        if existing_user_email:
            raise ValidationError(
                'That email already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField(validators=[
                           InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print(user.password)
            print(form.password.data)
            if werkzeug.security.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/user_listings')
    return render_template('login.html', form=form)





@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = werkzeug.security.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route("/listings")
def all_listings():
    """show all the apartment listings"""
    API_KEY = os.environ['YELP_KEY']
    URL = 'https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}

    # Define the Parameters of the search
    zip_code = request.args.get('zipcode','')
    
    PARAMS = {'location':zip_code,
              'categories':'apartments',
              'limit':50}
   

    # Make a Request to the API, and return results
    response = requests.get(url=URL, 
                            params=PARAMS, 
                            headers=HEADERS)
    

    # Convert response to a JSON String
    listings_data = response.json()  

    if 'businesses' in listings_data:
        listing_results = listings_data['businesses']
    else:
        listing_results = []
    

    #data from database
    db_results = crud.get_listing_from_db(zip_code)
    
    #data count from yelp_api and database
    data_count = 50 + len(db_results)
    

    return render_template('all_listings.html', pformat=pformat,listings_data=listings_data,listing_results=listing_results,db_results=db_results,data_count=data_count)

@app.route("/add_listing")
# @login_required
def add_listing():
    return render_template('add_listing.html')


@app.route("/user_listings")
# @login_required
def get_user_listings():
    """Show all user listings"""
    if request.method == 'GET':
        user_listings = crud.get_all_listings()
        return render_template('user_listings.html', user_listings = user_listings)

@app.route("/user_listings", methods=['POST'])
# @login_required
def add_user_listings():
    """create a new user listing"""
    if request.method =='POST':
        name = request.form.get("add_name")
        phone = request.form.get("add_phone")
        street_address = request.form.get("add_address")
        city = request.form.get("add_city")
        state = request.form.get("add_state")
        rating = request.form.get("add_rating")
        zip_code = int(request.form.get("add_zip_code"))
        image_url = request.form.get("add_image_url")
        user_id = request.form.get("add_user_id")

        #combining information for address to match the data format of yelp_api
        address = f"{street_address},{city},{state}"

        new_listing = crud.create_listing(name,rating,address,zip_code,phone,image_url,user_id,yelp_id='')
        db.session.add(new_listing)
        db.session.commit()
        flash("New Listing created!")
        user_listings = crud.get_all_listings()

        # if 'user_email' in session:
        #     submitter = session['user_email']
        #     new_listing = crud.create_listing(name,rating,address,zip_code,phone,image_url,submitter)
        # else:
        #     flash("Please log in or register an account!")
        #     redirect("/")

        return render_template('user_listings.html',user_listings=user_listings)





if __name__ == "__main__":
    connect_to_db(app,'favorites')
    app.run(host="0.0.0.0", debug=True)

