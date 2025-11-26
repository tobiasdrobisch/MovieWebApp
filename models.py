"""
Database models for the Movie Web App.

Defines SQLAlchemy ORM models for User and Movie entities.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    Represents a registered user in the application.

    Attributes:
        id (int): Primary key.
        name (str): Name of the user.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Establish relationship to Movie (not required but helpful)
    movies = db.relationship("Movie", backref="user", cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"<User id={self.id} name='{self.name}'>"


class Movie(db.Model):
    """
    Represents a movie marked as a user's favorite.

    Attributes:
        id (int): Primary key.
        name (str): Movie title.
        director (str): Name of the film's director.
        year_of_release (int): Year the film was released.
        poster_url (str): Link to the movie's poster.
        user_id (int): Foreign key referencing the owning User.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=True)
    year_of_release = db.Column(db.Integer, nullable=True)
    poster_url = db.Column(db.String(200), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Movie id={self.id} name='{self.name}' user_id={self.user_id}>"
