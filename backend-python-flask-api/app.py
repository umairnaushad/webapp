import sys

from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import DATABASE_URI

db2 = create_engine(DATABASE_URI)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

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

@app.route('/')
def show_all():
   return render_template('layout.html')
   #return render_template('show_all.html', users = User.query.all() )

@app.route('/home')
def home():
   return render_template('show_all.html', users = User.query.all() )

@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/new', methods = ['GET', 'POST'])
@app.route('/register', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      req = request.form
      username = req.get("username")
      email = req.get("email")
      print("username = " + str(username))
      print("email = " + str(email))
      if not username or not email:
         flash('Please enter all the fields', 'error')
      else:
         user = User(username, email)
         db.session.add(user)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   else:
      return render_template('new.html')

@app.route('/api/v1/resources/users/all', methods=['GET'])
@app.route('/all', methods=['GET'])
def users_all():
   result_set = db2.execute("SELECT * FROM user")
   return jsonify(result_set)

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)