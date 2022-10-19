import imp
import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from user import User
from app import app, get_current_user


@app.route('/profile', methods = ['GET'])
def profile():
    user = get_current_user()
    return render_template('profile.html', username=user.username)