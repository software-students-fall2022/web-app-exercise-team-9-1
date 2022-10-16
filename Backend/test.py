import pymongo
from bson.objectid import ObjectId
import datetime

connection = pymongo.MongoClient("mongodb+srv://admin:12345678!!@cluster0.yfbfkgx.mongodb.net/?retryWrites=true&w=majority")
db = connection["Amusement_Park_Rides"]

doc = {
    "Username": "test_db",
    "Passwprd": "test_pwd"
}

mongoid = db.Users.insert_one(doc)
print("test")