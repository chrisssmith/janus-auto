from pymongo import MongoClient
import datetime
import secrets
global collection
global db

def db_init():
    # This sets the db and collection will be used
    client = MongoClient()
    db = client.secrets.db
    collection = db.secrets.collection

client = MongoClient()

db = client.secrets.db
collection = db.secrets.collection
def insert_to_db(data):
    # This function takes a python dictionary and inserts the data into Mongodb
    post_id = collection.insert_one(data).inserted_id



def empty_db():
    #This purges all documents in the collection
    collection.delete_many({})

