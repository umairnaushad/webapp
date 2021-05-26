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
   print("username="+str(username)+"-email="+str(email))
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


##################################

@app.route('/api/v1/resources/users', methods=['GET'])
def getAllUsers():
   return getUsers()

@app.route('/api/v1/resources/users/ById/<int:id>', methods=['GET'])
def getUserById(id):
   if request.method == 'GET':
      return getUserById(id)

@app.route('/api/v1/resources/users/ByUsername/<string:name>', methods=['GET'])
def getUserByName(name):
   if request.method == 'GET':
      return getUserByUsername(name)

####################


@app.route('/api/v1/resources/users/users/create', methods=['POST'])
def createUser():
   if request.method == 'POST':
      session.add(User(request.form.get("username"), request.form.get("email")))
      session.commit()
      return redirect(url_for('getAllUsers'))

'''
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
'''

@app.route('/')
@app.route('/userApi', methods = ['GET', 'POST'])
def booksFunction():
   req = request.form
   username = req.get("username")
   email = req.get("email")
   if request.method == 'GET':
      return getUsers()
   elif request.method == 'POST':
      print("POST")      
      print("username=" + str(username))
      print("email=" + str(email))
      newUser = User(username, email)
      session.add(newUser)
      session.commit()
      #return jsonify(User=newUser.serialize)
      return render_template('user.html', users=newUser, isList="false")




def addNewUser(userName, email):
   newUser = User(username=userName, email=email)
   session.add(newUser)
   session.commit()
   return jsonify(User=newUser.serialize)

################################

def getUsers():
   users = session.query(User).all()
   return jsonify(users= [user.serialize for user in users])

def getUserById(user_id):
   users = session.query(User).filter_by(id = user_id).one()
   return jsonify(users= users.serialize)

def getUserByUsername(username):
   users = session.query(User).filter_by(username = username).all()
   return jsonify(users= [user.serialize for user in users])

if __name__ == '__main__':
   Base.metadata.create_all(engine)
   app.run(debug = True)