import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from user import User

##Establishing a connection to the database
connection = pymongo.MongoClient("mongodb+srv://admin:12345678!!@cluster0.yfbfkgx.mongodb.net/?retryWrites=true&w=majority")
db = connection["Amusement_Park_Rides"]

print("test")

##Creating the Flask instance
app = Flask(__name__)
app.secret_key = "secret key"

##Binds Flask log-in to the server
login_manager = LoginManager()
login_manager.init_app(app)

##Returns the current user with their properties
@staticmethod
def get_current_user():
    if current_user.is_authenticated:
        return User(id = current_user.id, username = current_user.username)
    return None

##Sends user back to home screen
def check_authentification_in_app():
    if not current_user.is_authenticated: 
        return redirect(url_for('home'))

##Importing .py files for profile, opening, and main page
import profile
import opening
import main_page
import editor


##Route to original url (home page)
##Redirect to home page
@app.route('/')
def home():
    if current_user.is_authenticated: 
        return redirect(url_for('main_page'))
    return render_template('opening.html',opec=0, msg="")


##Route to test page (accepts post requests)
##Loads test.html as the home page
@app.route('/test', methods = ['POST'])
def show_home():
   return render_template('test.html')

@login_manager.user_loader
def load_user(id):
    user = db.Users.find_one({"_id": id })
    if not user:
        return None
    return User(id = user['_id'], username = user['Username'])








##Route to logout page (accepts post and get requests)
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

app.run(debug = True)