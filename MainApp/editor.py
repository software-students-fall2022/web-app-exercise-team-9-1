import imp
import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from user import User
from app import app, get_current_user, db,check_authentification_in_app

##
@staticmethod
##def 

@app.route('/editor')
def editor():
    check_authentification_in_app()

    users = db.Users.find({ _UserType: 1 });
    if (current_user in users) {
        ## where the front end is rendered
    }



