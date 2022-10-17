import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from user import User



connection = pymongo.MongoClient("mongodb+srv://admin:12345678!!@cluster0.yfbfkgx.mongodb.net/?retryWrites=true&w=majority")
db = connection["Amusement_Park_Rides"]

print("test")

app = Flask(__name__)
app.secret_key = "secret key"

login_manager = LoginManager()
login_manager.init_app(app)

@staticmethod
def get_current_user():
    if current_user.is_authenticated:
        return User(id = current_user.id, username = current_user.username)
    return None



import profile
import opening



@app.route('/')
def home():
    if current_user.is_authenticated: 
        return redirect(url_for('profile'))
    return render_template('opening.html',opec=0, msg="")

 
 
@app.route('/test', methods = ['POST'])
def show_home():
   return render_template('test.html')

@login_manager.user_loader
def load_user(id):
    user = db.Users.find_one({"_id": id })
    if not user:
        return None
    return User(id = user['_id'], username = user['Username'])


def check_authentification_in_app():
    if not current_user.is_authenticated: 
        return redirect(url_for('home'))






@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

app.run(debug = True)