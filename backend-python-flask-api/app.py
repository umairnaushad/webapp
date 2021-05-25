import sys

from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import DATABASE_URI

from base import Session, engine, Base
from user import User

##db2 = create_engine(DATABASE_URI)

app = Flask(__name__)
##app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = "abcabcabc"

##db = SQLAlchemy(app)

"""
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __init__(self, username, email):
           self.username=username
           self.email=email

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
"""
@app.route('/')
def show_all():
   return render_template('layout.html')
   #return render_template('show_all.html', users = User.query.all() )

@app.route('/home')
def home():
   session = Session()
   users = session.query(User).all()
   session.close()
   return render_template('show_all.html', users = users)
   #return render_template('show_all.html', users = User.query.all() )

@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/new', methods = ['GET', 'POST'])
@app.route('/register', methods = ['GET', 'POST'])
def new():
   req = request.form
   username = req.get("username")
   email = req.get("email")
   if request.method == 'POST':
      if not username or not email:
         flash('Please enter all the fields', 'error')
      else:
         session = Session()
         user = User(username, email)
         session.add(user)
         session.commit()
         session.close()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   else:
      return render_template('new.html')

@app.route('/api/v1/resources/users', methods=['GET'])
def get_users():
   if 'username' in request.args:
      name = request.args['username']
   session = Session()
   users = session.query(User).filter_by(username=name).all()
   session.close()
   return render_template('show_all.html', users = users)
   #return jsonify(users)

if __name__ == '__main__':
   Base.metadata.create_all(engine)
   app.run(debug = True)