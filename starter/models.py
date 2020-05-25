import os
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate


# database_path ='postgres://fardeen:admin@localhost/castingagency'
# #database_path =os.environ.get('DATABASE_URL')
# db = SQLAlchemy()

database_name = "castingagency"
#database_path = "postgres://{}:{}@{}/{}".format('fardeen', 'admin','localhost', database_name)
#DATABASE_URL: postgres://rjenpkjzvezxst:e723216912da6a6fb504cc5fc28dd82c87b9cd1167a038480e6e794893666dab@ec2-35-169-254-43.compute-1.amazonaws.com:5432/d6uibri7fkbi86
database_path=os.environ.get('DATABASE_URL')


db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.create_all()
    #migrate = Migrate(app,db)
    with app.app_context():
      db.create_all()


castingagencydata = db.Table('castingagencydata', Column('actor_id', Integer, ForeignKey('actor.id', ondelete='CASCADE'), primary_key=True), Column('movie_id', Integer, ForeignKey('movie.id', ondelete='CASCADE'), primary_key=True))

class Movie(db.Model):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    release_date = Column(String(120),nullable=False)


    def __init__(self, title, release_date):
      self.title = title
      self.release_date = release_date

    def insert(self):
      db.session.add(self)
      db.session.commit()
  
    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
      return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date
      }


class Actor(db.Model):
    __tablename__ = 'actor'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(120),nullable=False)
    movies = relationship('Movie', secondary=castingagencydata, backref='actors')

    def __init__(self, name, age, gender):
      self.name = name
      self.age = age
      self.gender = gender
      

    def insert(self):
      db.session.add(self)
      db.session.commit()
  
    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
      return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender,
      }


