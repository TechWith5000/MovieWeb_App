
#This file implements the SQLiteDataManager class that interacts with the database.

from flask import Flask
from datamanager.data_models import db, User, Movie
from datamanager.data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app: Flask):
        self.app = app
        with self.app.app_context():
            db.init_app(app)
            db.create_all() #Only run once to establish database schema


    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, user_name):
        new_user = User(name=user_name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def add_movie(self, user_id, name, director, year, rating):
        new_movie = Movie(user_id=user_id, name=name, director=director, year=year, rating=rating)
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    def update_movie(self, movie_id, name=None, director=None, year=None, rating=None):
        movie = Movie.query.get(movie_id)
        if movie:
            if name:
                movie.name = name
            if director:
                movie.director = director
            if year:
                movie.year = year
            if rating:
                movie.rating = rating
            db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
        return movie
