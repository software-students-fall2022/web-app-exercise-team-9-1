import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response
import datetime

connection = pymongo.MongoClient("mongodb+srv://admin:12345678!!@cluster0.yfbfkgx.mongodb.net/?retryWrites=true&w=majority")
db = connection["Amusement_Park_Rides"]

doc = {
    "Username": "test_db",
    "Password": "test_pwd"
}

mongoid = db.Users.insert_one(doc)
print("test")

app = Flask(__name__)

@app.route('/')
def home():
    #docs = db.exampleapp.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    return render_template('index.html') # render the hone template

 
@app.route('/test', methods = ['POST'])
def show_home():
   return render_template('test.html')

app.run(debug = True)