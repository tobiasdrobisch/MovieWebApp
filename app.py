"""
Main Flask application module.

Initializes the Flask app, configures the database, and defines
all routes for managing users and their favorite movies.
"""

import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from data_manager import DataManager
from models import db, Movie, User


app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(DATA_DIR, 'movies.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Initialize DataManager
data_manager = DataManager()


@app.route("/users", methods=["POST"])
def create_user():
    """
    Create a new user and redirect to the index page.
    """
    user_input = request.form.get("user")

    if not user_input:
        flash("User name cannot be empty.", "error")
        return redirect(url_for("index"))

    data_manager.create_user(user_input)
    flash(f"User '{user_input}' added successfully!", "success")

    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/", methods=["GET"])
def get_movies(user_id):
    """
    Display a specific user's favorite movies.
    """
    user = User.query.get_or_404(user_id)
    movies = data_manager.get_movies(user_id)

    return render_template("users.html", user=user, movies=movies)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    """
    Add a new movie to a user's favorite movie list.
    """
    title = request.form.get("movie")
    director = request.form.get("director") or "Unknown"
    year = request.form.get("year")
    poster_url = request.form.get("poster_url")

    new_movie = Movie(
        name=title,
        director=director,
        year_of_release=year,
        poster_url=poster_url,
        user_id=user_id,
    )

    data_manager.add_movie(new_movie)
    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_movie(user_id, movie_id):
    """
    Update the title of an existing movie.
    """
    new_title = request.form.get("title")
    data_manager.update_movie(movie_id, new_title)

    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    """
    Delete a movie from a user's list of favorite movies.
    """
    data_manager.delete_movie(movie_id)
    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/")
def index():
    """
    Display a list of all users.
    """
    users = data_manager.get_users()
    return render_template("index.html", users=users)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run()
