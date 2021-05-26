import sys

from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from sqlalchemy.sql.functions import user
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

@app.route('/register', methods = ['GET', 'POST'])
def register():
   username = request.form.get("username")
   email = request.form.get("email")
   if request.method == 'POST':
      if not username or not email:
         flash('Please enter all the fields', 'error')
      else:
         user = User(username, email)
         session.add(user)
         session.commit()
         flash('Record was successfully added')
         return render_template('user.html', users=user, isList="false")
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

##################################

@app.route('/api/v1/resources/users/<int:user_id>/delete/', methods=['POST'])
def deleteUser(user_id):
    if request.method == 'POST':
      return deleteUser(user_id)

@app.route("/api/v1/resources/users/<int:user_id>/update/", methods=['POST'])
def updateUser(user_id):
    updateUser = session.query(User).filter_by(id=user_id).one()
    if request.method == 'POST':
        if request.form['email']:
            updateUser.email = request.form['email']
            return redirect(url_for('getAllUsers'))


####################


@app.route('/api/v1/resources/users/users/create', methods=['POST'])
def createUser():
   if request.method == 'POST':
      print("a="+str(request.form.get("username")))
      addNewUser(request.form.get("username"), request.form.get("email"))
      return redirect(url_for('getAllUsers'))


def addNewUser(userName, email):
   user = User(username=userName, email=email)
   session.add(user)
   session.commit()
   print("b="+str(user.email))
   getUserByUsername(userName)
   return jsonify(User=user.serialize)

################################

def getUsers():
   users = session.query(User).all()
   return jsonify(users= [user.serialize for user in users])

def getUserById(user_id):
   user = session.query(User).filter_by(id = user_id).one()
   return jsonify(user= user.serialize)

def getUserByUsername(username):
   users = session.query(User).filter_by(username = username).all()
   return jsonify(users= [user.serialize for user in users])

def updateUser(id, username, email):
    updatedUser = session.query(User).filter_by(id=id).one()
    if not username:
        updatedUser.username = User
    if not email:
        updatedUser.email = email
    session.add(updatedUser)
    session.commit()
    return 'Updated User with id %s' % id

def deleteUser(id):
    userToDelete = session.query(User).filter_by(id=id).one()
    session.delete(userToDelete)
    session.commit()
    return jsonify(
        status='success',
        id=userToDelete.id,
        username=userToDelete.username,
        email=userToDelete.email
    ), 200

if __name__ == '__main__':
   Base.metadata.create_all(engine)
   app.run(debug = True)