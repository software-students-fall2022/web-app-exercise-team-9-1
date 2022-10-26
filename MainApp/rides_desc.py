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
   
    ride_id = request.args.get('id')
    return show_rides_desc(ride_id)

@app.route('/rides_desc_post_rate', methods=['POST'])
def rides_desc_rate():
    check_authentification_in_app()
   
   
    ride_id = request.form.get('id')
    rate = int(request.form.get('rate_num'))
    
    currUser = get_current_user()
    currUserId = currUser.get_id()
    
    db.Rides.update({'_id': ride_id}, {'$pull': {'Popularity': {'User_ID': currUserId}}})
    print("testtt")
    db.Rides.update({'_id': ride_id}, {'$push': {'Popularity': {'User_ID': currUserId, 'Rating': rate}}})
    
   
    return redirect(url_for('rides_desc', id = ride_id))

    
@app.route('/rides_desc_post_comment', methods=['POST'])
def rides_desc_comment():
    check_authentification_in_app()
   
   
    ride_id = request.form.get('id')
    
    comment = request.form.get('comment')
    currUser = get_current_user()
    currUserId = currUser.get_id()
    db.Rides.find_one_and_update({'_id': ride_id}, {'$push': {'Feedbacks': {
                                    'User_ID': currUserId, 'Feedback': comment}}})
    return redirect(url_for('rides_desc', id = ride_id))
 
 
@app.route('/rides_delete', methods=['POST'])
def delete_ride():
    check_authentification_in_app()
   
    ride_id = request.form.get('id')
    
    db.Rides.delete_one({'_id': ride_id})
    return redirect(url_for('home'))

       
@app.route('/add_favorite_desc', methods=['POST'])
def add_favorite_rides_desc():
    print("add_favorite_rides_desc")
    check_authentification_in_app()

    ride_id = request.form.get('id')
    user = get_current_user()
    db.Users.update(
        { "_id": user.id },
        { "$push":  {'FavoriteRides': ride_id }})
    return show_rides_desc(ride_id)

@app.route('/remove_favorite_desc', methods=['POST'])
def remove_favorite_rides_desc():
    check_authentification_in_app()

    ride_id = request.form.get('id')
    user = get_current_user()
    db.Users.update(
        { "_id": user.id },
        { "$pull":  {'FavoriteRides': ride_id }})
    return show_rides_desc(ride_id)



class feedbackItem:
    def __init__(self, feedback, user_id, db):
        self.feedback = feedback
        user = db.Users.find_one({'_id': user_id})
        if user is not None:
             self.name = db.Users.find_one({'_id': user_id})['Name']
        else:
            self.name = user_id
    
def show_rides_desc(ride_id):
    rideObj = db.Rides.find_one({'_id': ride_id})
    user = get_current_user()
    
    user = db.Users.find_one({"_id": user.id})
    ride_desc = rideObj['Description']
    ride_bg = get_ride_bg_name(ride_id)
    ride_type = rideObj['RideType']
    ride_name = rideObj['Name']
    feedbacks = rideObj['Feedbacks']
    feedbackItems = []
    liked = ride_id in user['FavoriteRides']
    rate =  db.Rides.find_one({'_id': ride_id}, {'Popularity': {'$elemMatch': {'User_ID': user['_id']}}})
    
    for feedback in feedbacks:
        feedbackItems.append(feedbackItem(feedback['Feedback'], feedback['User_ID'], db))
    
    if(rate == None):
        rate = 0
    else:
        rate=1
        
    if (user['UserType'] == 0):
        
        return render_template('ride_user.html', ride_name=ride_name, ride_id=ride_id, ride_desc=ride_desc, ride_bg=ride_bg, ride_type=ride_type, feedbacks=feedbackItems, liked= liked, rate=rate)
    else:
        return render_template('ride_admin.html', ride_name=ride_name, ride_id=ride_id, ride_desc=ride_desc, ride_bg=ride_bg, ride_type=ride_type, feedbacks=feedbackItems)