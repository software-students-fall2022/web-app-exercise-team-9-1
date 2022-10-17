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

@app.route('/')
def home():
    if current_user.is_authenticated: 
        return redirect(url_for('profile'))
    return render_template('index.html') # render the hone template

 
@app.route('/test', methods = ['POST'])
def show_home():
   return render_template('test.html')

@login_manager.user_loader
def load_user(id):
    user = db.Users.find_one({"_id": id})
    if not user:
        return None
    return User(id = user['_id'], username = user['Username'])


@app.route('/login', methods = ['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('profile'))
   
    name = request.form.get('username')
    password = request.form.get('password')
    
   
    user = db.Users.find_one({"Username": name})
    #print("Password: ", password, "Correct Password: ", user['Password'])
    if user and user['Password'] == password:
        print("user found")
        user_obj = User(id = user['_id'], username = user['Username'])
        login_user(user_obj)
        flash("Success")
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('profile'))
    else:
        flash("Invalid username or password")
        
    return render_template('test.html', title = 'Sign In', form = request.form)
    

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/'))

app.run(debug = True)