import imp
import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import json
# from MainApp.main_page import get_ride_bg_name

from main_page import get_ride_bg_name
from user import User
from app import app, get_current_user, db, check_authentification_in_app


@app.route('/rides_desc', methods=['GET', 'POST'])
def rides_desc():
    check_authentification_in_app()
    if request.method == 'GET':
        ride_id = request.args.get('id')
        rideObj = db.Rides.find_one({'_id': ride_id})
        print('from get', rideObj)
    elif request.method == 'POST':
        print('post msg is', request.form)
        reqDict = request.form
        ride_id = request.form.get('ride_id')
        print('id from post', ride_id)
        rideObj = db.Rides.find_one({'_id': ride_id})
        print('from post', rideObj)

    user = get_current_user()
    user = db.Users.find_one({"_id": user.id})
    ride_desc = rideObj['Description']
    ride_bg = get_ride_bg_name(ride_id)
    ride_type = rideObj['RideType']
    ride_name = rideObj['Name']
    feedbacks = rideObj['Feedbacks']
    print(feedbacks)
    if request.method == 'POST':
        comment = request.form.get('comment')
        currUser = get_current_user()
        currUserId = currUser.get_id()
        db.Rides.find_one_and_update({'_id': ride_id}, {'$push': {'Feedbacks': {
                                     'User_ID': currUserId, 'Feedback': comment}}})
    if request.method == 'GET':
        if (user['UserType'] == 0):
            return render_template('ride_user.html', ride_name=ride_name, ride_id=ride_id, ride_desc=ride_desc, ride_bg=ride_bg, ride_type=ride_type, feedbacks=feedbacks)
        else:
            return render_template('ride_admin.html', ride_name=ride_name, ride_id=ride_id, ride_desc=ride_desc, ride_bg=ride_bg, ride_type=ride_type, feedbacks=feedbacks)
    else:
        return redirect(url_for('main_page'))
