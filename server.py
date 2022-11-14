"""Server for movie ratings app."""

from pprint import pformat

from flask import Flask, render_template, request, flash, session, redirect,url_for,jsonify
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
        user = User.query.filter_by( email=form.email.data).first()
        if user:
            if werkzeug.security.check_password_hash(user.password, form.password.data):
                login_user(user)
                session["user_email"] = user.email
                return redirect('/user_listings')
        flash("The email or password you entered was incorrect, please try again!")
    return render_template('login.html', form=form)





@app.route('/logout', methods=['GET', 'POST'])
# @login_required
def logout():
    logout_user()
    session.pop('user_email')
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = werkzeug.security.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


API_KEY = os.environ['YELP_KEY']

@app.route("/listings")
def all_listings():
    """show all the apartment listings"""
    
    URL = 'https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}  

    # Define the Parameters of the search
    # zip_code = request.args.get('zipcode','')

    if request.args.get('zipcode'):
        zip_code = request.args.get('zipcode')
        session['zip_code'] = zip_code
    elif session.get('zip_code'):
        zip_code = session['zip_code']
    else:
        zip_code = ''

    if zip_code == '':
        return redirect("/")
    else:
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

        if 'user_email' in session:
            user_id = crud.get_user_by_email(session['user_email']).id
        else:
            user_id = None
           

        return render_template('all_listings.html', pformat=pformat,listings_data=listings_data,listing_results=listing_results,db_results=db_results,data_count=data_count, user_id=user_id)

@app.route("/listings/<listing_id>")
def show_listing_details(listing_id):
    """Show details on a particular listing."""
    if listing_id.isdigit()  :
        db_listing = crud.get_listing_by_id(listing_id)
        yelp_listing = None
    else:
        db_listing = None
        URL = f"https://api.yelp.com/v3/businesses/{listing_id}"
        HEADERS = {'Authorization': 'bearer %s' % API_KEY}  
   

        # Make a Request to the API, and return results
        response = requests.get(url=URL, 
                            headers=HEADERS)
    

        # Convert response to a JSON String
        yelp_listing = response.json()  

    return render_template("listing_details.html", db_listing=db_listing,yelp_listing = yelp_listing)

@app.route("/add_listing")
@login_required
def add_listing():
    user_email = session.get("user_email","")
    user_id = crud.get_user_by_email(user_email).id
    return render_template('add_listing.html',user_id=user_id)

@app.route("/add_to_my_list", methods=['POST'])
@login_required
def add_to_my_list():
    """Add listing from home page to user listing page"""
    name = request.form.get("add_name")
    phone = request.form.get("add_phone")
    street_address = request.form.get("add_address")
    city = request.form.get("add_city")
    state = request.form.get("add_state")
    rating = request.form.get("add_rating")
    zip_code = int(request.form.get("add_zip_code"))
    image_url = request.form.get("add_image_url")
    yelp_id = request.form.get("add_yelp_id")
    submitter = request.form.get("submitter")
    

    #combining information for address to match the data format of yelp_api
    address = f"{street_address},{city},{state}"
    # find user through its email
    user_email = session.get("user_email","")
    user_id = crud.get_user_by_email(user_email).id

    if submitter != str(user_id):
        new_listing = crud.create_listing(name,rating,address,zip_code,phone,image_url,user_id,yelp_id)
        db.session.add(new_listing)
        db.session.commit()
        flash("New Listing Added!")
        db.session.close()
    
        user_listings = crud.get_listing_by_user_email(user_email)
        listing_count = len(user_listings)

        return render_template('user_listings.html',user_listings=user_listings,listing_count=listing_count)
    else:
        return redirect("/")


@app.route("/post_listing",  methods=['POST'])
@login_required
def post_new_listing():
    """add new listing to user listing page"""
    name = request.form.get("add_name")
    phone = request.form.get("add_phone")
    street_address = request.form.get("add_address")
    city = request.form.get("add_city")
    state = request.form.get("add_state")
    rating = request.form.get("add_rating")
    zip_code = int(request.form.get("add_zip_code"))
    image_url = request.form.get("add_image_url")
    yelp_id = request.form.get("add_yelp_id")
    

    #combining information for address to match the data format of yelp_api
    address = f"{street_address},{city},{state}"
    # find user through its email
    user_email = session.get("user_email","")
    user_id = crud.get_user_by_email(user_email).id

    new_listing = crud.create_listing(name,rating,address,zip_code,phone,image_url,user_id,yelp_id)
    db.session.add(new_listing)
    db.session.commit()
    flash("New Listing Added!")
    db.session.close()
    
    user_listings = crud.get_listing_by_user_email(user_email)
    listing_count = len(user_listings)

    return render_template('user_listings.html',user_listings=user_listings,listing_count=listing_count)

   
        

@app.route("/user_listings") 
@login_required
def show_user_listing() :
    """show all user listings"""
    user_email = session.get("user_email","")
    try:
        user_listings = crud.get_listing_by_user_email(user_email)
    except:
        flash("There is no listing yet.")
        user_listings = []
        # return render_template('user_listings.html',user_listings=user_listings)
    else:
        user_listings = crud.get_listing_by_user_email(user_email)
        listing_count = len(user_listings)
        # return render_template('user_listings.html',user_listings=user_listings)
    finally:
        return render_template('user_listings.html',user_listings=user_listings,listing_count=listing_count)

@app.route("/user_listings/favorite.json", methods=['POST'])
@login_required
def set_favorite():
    """set listing as favorite listing"""
    listing_id = int(request.json.get('listing_id'))
    print(listing_id)
    listing = crud.get_listing_by_id(listing_id)
    print(listing)

    if listing:
        result_text = f"{listing.name} is your favorite listing!"
    else:
        result_text = "There is no favorite listing yet."

    return jsonify({'msg': result_text})





if __name__ == "__main__":
    connect_to_db(app,'favorites')
    app.run(host="0.0.0.0", debug=True)

