"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Show homepage""" 

    return render_template('homepage.html')

#best practice to create as few routes as possible;
@app.route('/users')
def get_users():
    """Show Users Page""" 

    users = crud.get_all_users()

    return render_template('users.html', users=users)


@app.route('/users', methods = ["POST"])
def register_user():
    """Create a new user."""
    email = request.form.get("email")
    password=request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("You have an account. Please login.")
    #you cannd create an count OR please login (Redircet to login palge)
    else: 
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route('/login', methods = ['POST'])
def login_user():
    """Log in User"""
    email = request.form.get("email")
    password=request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or user.password != password: 
        flash("The email or password you entered was incorrect!")
    else:
        session['user_email'] = user.email
        flash(f"Welcome back, {user.email}")
    
    return redirect("/")


@app.route('/users/<user_id>')
def show_user(user_id):

    user = crud.get_user_by_id(user_id)
    # print(movie)

    return render_template('user_details.html', user = user)



@app.route('/movies')
def all_movies():
    """"Shows all the movies"""
    movies = crud.get_all_movies()

    return render_template('all_movies.html', movies=movies) 


@app.route('/movies/<movie_id>')
def show_movie(movie_id):

    movie = crud.get_movie_by_id(movie_id)
    # print(movie)

    return render_template('movie_details.html', movie = movie)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
