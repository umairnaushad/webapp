import sys

from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from base import Session, engine, Base
from user import User
from config import DATABASE_URI

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcabcabc"
session = Session()

@app.route('/')
def default():
   return render_template('layout.html')

@app.route('/home')
def home():
   users = session.query(User).all()
   session.close()
   return render_template('user.html', users = users)

@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/register', methods = ['GET', 'POST'])
def new():
   req = request.form
   username = req.get("username")
   email = req.get("email")
   if request.method == 'POST':
      if not username or not email:
         flash('Please enter all the fields', 'error')
      else:
         user = User(username, email)
         session.add(user)
         session.commit()
         flash('Record was successfully added')
         return render_template('user.html', users=user, isList="false")
         #return redirect(url_for('user'))
   return render_template('register.html')

@app.route('/api/v1/resources/users', methods=['GET'])
def get_users():
   if 'username' in request.args:
      name = request.args['username']
   #session = Session()
   users = session.query(User).filter_by(username=name).all()
   session.close()
   return render_template('user.html', users = users, isList="true")
   #return jsonify(users)

if __name__ == '__main__':
   Base.metadata.create_all(engine)
   app.run(debug = True)