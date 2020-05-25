import os
from flask import Flask, request, abort, jsonify , render_template, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from models import Movie, Actor, setup_db, db
from auth import AuthError, requires_auth , get_token_auth_header

def create_app(test_config=None):
  app = Flask(__name__, template_folder='./templates')
  CORS(app)
  setup_db(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, DELETE, OPTIONS')
    return response 

  
  #redirect to login page 
  @app.route('/', methods=['GET','DELETE'])
  def index():
    return render_template('index.html')

  #login page API 
  @app.route('/login', methods=['GET','POST'])
  def login():
    return render_template("index.html")

  #login page call back API 
  @app.route('/user-page', methods=['GET','POST'])
  def user_logged():
    return render_template("afterlogin.html")

  #list all the actors 
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(jwt):
    actors = Actor.query.all()
    formatted_actors = [actor.format() for actor in actors]
    if len(formatted_actors) == 0:
      abort(404)

    return jsonify({
      'success': True ,
      'actors' : formatted_actors ,
      'total_actors' : len(formatted_actors)
    })
   
  # adding a new actor 
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_new_actor(jwt): 
    body = request.get_json()
    if not ('name' in body and 'age' in body and 'gender' in body):
      abort(422)

    name=body.get('name')
    age=body.get('age')
    gender=body.get('gender')

    try:
      actor=Actor(name=name, age=age, gender=gender)
      actor.insert()
      return jsonify({
        "success": True,
        "actor":[actor.format()]
      })
    except:
      abort(422)
  
  # updating  a specifc actor 
  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(jwt, id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if actor:
      try:
        body = request.get_json()
        name=body.get('name')
        age=body.get('age')
        gender=body.get('gender')

        if name:
          actor.name=name
        if age:
          actor.age=age
        if gender:
          actor.gender=gender

        actor.update()
        return jsonify({
          "success": True,
          "actor": [actor.format()]
        })

      except:
        abort(422)
    else:
      abort(404)

  #deleting a specific actor 
  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, id):
    actor=Actor.query.get(id)
    if actor:
      try:
        actor.delete()
        return jsonify({
          "success":True,
          "delete":id
        })
      except:
        abort(422)
    else:
      abort(404)

  #listing all the movies 
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(jwt):   
    movies = Movie.query.all()
    formatted_movies = [movie.format() for movie in movies]
    if len(formatted_movies) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'movies' : formatted_movies,
      'total_movies' : len(formatted_movies)
    })

  # adding a new movie 
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_new_movie(jwt): 
    body = request.get_json()
    if not('title' in body and 'release_date' in body):
      abort(422)
    title= body.get('title')
    release_date= body.get('release_date')

    try:
      movie=Movie(title=title, release_date=release_date)
      movie.insert()
      movies=Movie.query.all()
      formatted_movies = [movie.format() for movie in movies]
      return jsonify({
        "success": True,
        "movies": [movie.format()],
        "created":movie.id,
        "total_movies":len(formatted_movies)
      })
    except:
      abort(422)
      
  #editing an exist movie 
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(jwt, id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if movie:
      try:
        body=request.get_json()
        title=body.get('title')
        release_date=body.get('release_date')

        if title:
          movie.title=title

        if release_date:
          movie.release_date=release_date

        movie.update()
        return jsonify({
          "success": True,
          "updated_movie_id":id,
          "movie":[movie.format()]
        })

      except:
        abort(422)

    else:
      abort(404)


  # deleting a specifc movie 
  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt, id):
    movie=Movie.query.get(id)
    if movie:
      try:
        movie.delete()
        return jsonify({
          "success":True,
          "delete":id
        })
      except:
        abort(422)
    else:
      abort(404)



  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
    }), 422
 

  #Error Handeling 
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success" : False,
      "error" : 400,
      "message" : "bad request "
    }), 400

  @app.errorhandler(405)
  def method_not_found(error):
    return jsonify({
      "success" : False,
      "error" : 405 ,
      "message" : "Method not found "
    }), 405

  # @app.errorhandler(AuthError)
  # def handle_auth_error(ex):
  #      response = jsonify(ex.error)
  #      response.status_code = ex.status_code
  #      return response

  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
    return jsonify({
      "success": False,
      "error": ex.status_code,
      'message': ex.error
    }), 401


  return app

app = create_app()

# if __name__ == '__main__':
#     app.run()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
