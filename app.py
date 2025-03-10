
#This is the main Flask application file, handling routes and rendering templates.

from flask import flash, Flask, render_template, request, redirect, url_for
from datamanager.data_models import db
from datamanager.data_management import SQLiteDataManager
import os

# Flask app initialization
app = Flask(__name__)
app.secret_key = "very_secret_key"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "data_storage", "movies.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database and Data Manager
data_manager = SQLiteDataManager(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/users')
def users_list():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', movies=movies, user_id=user_id)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        data_manager.add_user(name)
        return redirect(url_for('users_list'))
    return render_template('add_user.html')

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        name = request.form['name']
        movie = data_manager.add_movie(user_id, name)
        if movie:
            flash("Movie added successfully!", "success")
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        name = request.form.get('name')
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')
        data_manager.update_movie(movie_id, name, director, year, rating)
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))

@app.errorhandler(404)
def page_not_found(error):
    """
    Handles the 404 error and renders the 404.html template.
    Arguments received:
        error: Error object.
    Returns:
        tuple: A tuple containing the rendered template and the HTTP status code.
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    Handles the 500 error and renders the 500.html template.
    Arguments received:
        error: Error object.
    Returns:
        tuple: A tuple containing the rendered template and the HTTP status code.
    """
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)



