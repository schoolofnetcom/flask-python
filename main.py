from flask import Flask, request, jsonify, render_template, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="public")

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/flask"
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(120))
  password = db.Column(db.String(120))

  def __init__(self, username, password):
    self.username = username
    self.password = password


@app.route('/<name>', methods = ['GET'])
def hello(name):
  users = User.query.order_by(User.username)
  json_users = []
  obj = {
    'username': users.username,
    'password': users.password
  }

  return jsonify(user = obj)
  # for user in users:
  #   obj = {
  #     'username': user.username,
  #     'password': user.password
  #   }

  #   json_users.append(obj)

  # return jsonify(users = json_users)

@app.route('/create', methods = ['POST'])
def create():
  user = User(request.form['username'], request.form['password'])

  db.session.add(user)

  obj = {
    'username' : request.form['username'],
    'password' : request.form['password']
  }

  db.session.commit()

  return jsonify(user = obj)


@app.route('/delete/<int:id>', methods = ['DELETE', 'POST'])
def delete(id):
  user = User.query.get(id)

  db.session.delete(user)
  db.session.commit()

  obj = {
    'id' : user.id
  }

  return jsonify(user = id)


@app.route('/edit/<int:id>', methods = ['PUT', 'POST', 'PATCH'])
def update(id):
  user = User.query.get(id)

  user.username = request.form['username']
  user.password = request.form['password']

  db.session.commit()

  obj = {
    'username': user.username,
    'password': user.password
  }

  return jsonify(user = obj)


@app.route('/')
def root():
  return "index"

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404