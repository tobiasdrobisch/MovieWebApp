"""
Data management module.

Provides a clean abstraction layer for all database CRUD operations
related to Users and Movies using SQLAlchemy ORM.
"""

from models import db, User, Movie


class DataManager:
    """
    Handles database operations for User and Movie models.
    """

    def create_user(self, name):
        """
        Create and store a new user.

        Args:
            name (str): The name of the user.
        """
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        """
        Retrieve all users from the database.

        Returns:
            list[User]: A list of User objects.
        """
        return User.query.all()

    def get_movies(self, user_id):
        """
        Retrieve all movies associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[Movie]: A list of Movie objects.
        """
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """
        Add a new movie to the database.

        Args:
            movie (Movie): The Movie object to store.
        """
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """
        Update the title of an existing movie.

        Args:
            movie_id (int): The ID of the movie to update.
            new_title (str): The new title.

        Returns:
            Movie | None: The updated movie, or None if not found.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_title
            db.session.commit()
            return movie
        return None

    def delete_movie(self, movie_id):
        """
        Delete a movie from the database.

        Args:
            movie_id (int): The ID of the movie to delete.

        Returns:
            bool: True if deleted, False if the movie was not found.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False
