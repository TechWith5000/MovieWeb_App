
#This file implements the SQLiteDataManager class that interacts with the database.

from flask import flash, Flask
from datamanager.data_models import db, User, Movie
from datamanager.data_manager_interface import DataManagerInterface
import requests
import os
from dotenv import load_dotenv


load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")


def fetch_movie_details(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            # Extract year safely
            year_str = data.get("Year", "0")
            try:
                year = int(year_str.split("–")[0])  # Take the first year if it's a range
            except ValueError:
                year = 0  # Default to 0 if conversion fails

            return {
                "name": data.get("Title", movie_name),
                "director": data.get("Director", "Unknown"),
                "year": year,
                "rating": float(data.get("imdbRating", 0))
            }
        else:
            flash("Movie not found in OMDb.", "warning")
    else:
        flash("Error fetching movie details from OMDb.", "danger")
    return None



class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app: Flask):
        self.app = app
        with self.app.app_context():
            db.init_app(app)
            #db.create_all() #Only run once to establish database schema


    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, user_name):
        new_user = User(name=user_name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def add_movie(self, user_id, name):
        movie_details = fetch_movie_details(name)
        if movie_details:
            new_movie = Movie(user_id=user_id, **movie_details)
            db.session.add(new_movie)
            db.session.commit()
            return new_movie
        return None

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
