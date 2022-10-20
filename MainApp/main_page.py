import imp
import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from user import User
from app import app, get_current_user, db,check_authentification_in_app

@staticmethod
def get_ride_type_name(ride_type_id):
    if(ride_type_id == 0):
        return "Slow-paced"
    elif (ride_type_id == 1):
        return "Moderate"
    elif (ride_type_id == 2):
        return "Intensive"
    elif (ride_type_id == 3):
        return "Interactive"
    elif (ride_type_id == 4):
        return "Sightseeing"
    elif (ride_type_id == 5):
        return "Others"
    return "Others"

@staticmethod
def get_maintenance_name(maintenance_id):
    if(maintenance_id == 0):
        return "Good"
    elif (maintenance_id == 1):
        return "Needs Work"
    elif (maintenance_id == 2):
        return "Heavy Duty"
    elif (maintenance_id == 3):
        return "Broken"
    return "Broken"

@staticmethod
def get_ride_bg_name(ride_type_id):
    
    return "url('../static/images/type" + str(ride_type_id)+".jpg')"

@app.route('/main_page')
def main_page():
    check_authentification_in_app()
    
    rides = db.Rides.find()
    return render_rides_list(rides, 'main_page.html', 'main_page_admin.html')
    
    
@app.route('/favorite', methods = ['GET'])
def favorite_rides():
    check_authentification_in_app()
    user = get_current_user()
    user = db.Users.find_one({"_id": user.id})
    favorite_ride_ids = user['FavoriteRides']
    rides = db.Rides.find({"_id": {"$in": favorite_ride_ids}})
    return render_rides_list(rides, 'favorite_rides.html', 'favorite_rides.html')

@app.route('/remove_favorite', methods = ['POST'])
def remove_favorite():
    check_authentification_in_app()
    user = get_current_user()
    
    removed_id = request.form.get('id')
    print("Removed ID: ", removed_id)
    
    db.Users.update(
        { "_id": user.id },
        { "$pull":  {'FavoriteRides': removed_id }})

    return favorite_rides()


@app.route('/search', methods = ['GET', 'POST'])
def search():
  
    check_authentification_in_app()
    search_string = request.args.get('search_text')
    print("Search String: ", search_string)
    rides = db.Rides.find({"$or": [{ 'Name' : { '$regex' : search_string, '$options' : 'i' }},
                                   { 'Description' : { '$regex' : search_string, '$options' : 'i' }}]})
    return render_rides_list(rides, 'search_page_user.html', 'search_page_admin.html')


    
def render_rides_list(rides, page_name_user,page_name_admin):
    user = get_current_user()
    user = db.Users.find_one({"_id": user.id})
    
    rideIDs = rides.distinct("_id")
    ride_names = []
    ride_type = []
    ride_desc =[]
    wait_times=[]
    height_req=[]
    ratings=[]
    maintence=[]
    ride_type_bg_name = []
    maintence_name = []
    
    for rideID in rideIDs:
        ride = db.Rides.find_one({"_id": rideID})
        ride_names.append(ride['Name'])
        ride_type.append(get_ride_type_name(ride['RideType']))
        ride_desc.append(ride['Description'])
        wait_times.append(ride['WaitTime'])
        height_req.append(ride['HeightRequirement'])
        #ride['Popularity'] is a list of objects, each object has a user id and a rating.
        #get the total number of ratings for the ride
        this_ratings = ride['Popularity']
        total_ratings_count = len(this_ratings)
        total_rating=0
        print("RideID: ", rideID, "Ratings: ")
        for rating in this_ratings:
            print(rating['Rating'])
            total_rating += rating['Rating']
        ratings.append(round(total_rating/total_ratings_count))
        maintence.append(ride['Maintenance'])
        maintence_name.append(get_maintenance_name(ride['Maintenance']))
        ride_type_bg_name.append(get_ride_bg_name(ride['RideType']))
    
    if(user['UserType'] == 0):
        return render_template(page_name_user, rideIDs=rideIDs, ride_names=ride_names, ride_type=ride_type, ride_desc=ride_desc, wait_time=wait_times, height_req=height_req, ratings=ratings, maintence=maintence,bg_names=ride_type_bg_name)
    
    return render_template(page_name_admin, rideIDs=rideIDs, ride_names=ride_names, ride_type=ride_type, ride_desc=ride_desc, wait_time=wait_times, height_req=height_req, ratings=ratings, maintence=maintence,bg_names=ride_type_bg_name, maintence_name=maintence_name)
    