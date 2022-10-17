import imp
import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from user import User
from app import app, get_current_user, db

@app.route('/sign_in', methods = ['POST'])
def opening_page():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    name = request.form.get('username')
    password = request.form.get('password')
    user = db.Users.find_one({"Username": name})
    if(name == "" or password == ""):
        return render_template('opening.html', opec=1, msg="Please fill in all the fields")
    
    if request.form['action'] == 'Login':
        if user and user['Password'] == password:
            print("user found")
            user_obj = User(id = user['_id'], username = user['Username'])
            login_user(user_obj)
            return redirect(url_for('profile'))
        else:
            return render_template('opening.html', opac=1, msg="Invalid username and/or password")
    else:
        if user:
            return render_template('opening.html', opac=1, msg="Username already exists")
        else:
            doc={
                "Username": name,
                "Password": password,
                "UserType": 0,
                "Name": name,
                "FavoriteRides": [],
                "_id": str(ObjectId())
            }
            db.Users.insert_one(doc)
            user = db.Users.find_one({"Username": name})
           
            user_obj = User(id = user['_id'], username = user['Username'])
           
            login_user(user_obj)
            return redirect(url_for('profile'))
            



    