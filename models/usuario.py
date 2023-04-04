from flask import jsonify
from pymongo import MongoClient
import os
from dotenv import find_dotenv, load_dotenv
from bson.objectid import ObjectId

load_dotenv(find_dotenv())

bd_username = os.environ.get("MONGODB_USER")
bd_password = os.environ.get("MONGODB_PWD")
connection_string = f'mongodb+srv://{bd_username}:{bd_password}@cluster.5ougas6.mongodb.net/?retryWrites=true&w=majority'


class UserModel:
    client = MongoClient(connection_string)
    db = client['apiwithmongo']
    try:
        db.validate_collection('Usuarios')
    except Exception as e:
        print(e)
        db.create_collection('Usuarios')
    users_collection = db['Usuarios']

    def __init__(self, username, password):
        self.object_id = ObjectId()
        self.username = username
        self.password = password

    def json(self):
        return {
            "username": self.username
        }

    @classmethod
    def find_user(cls, username):
        user = cls.users_collection.find_one({"username": username})
        if user:
            return user
        return None

    def save_user(self):
        self.users_collection.insert_one({
            "username": self.username,
            "password": self.password
        })
        return jsonify(self.json())

    def update_user(self):
        user = self.users_collection.update_one({"username": self.username}, {'$set': {
            "username": self.username,
            "password": self.password
        }
        })
        return user

    @classmethod
    def delete_user(cls, username):
        return cls.users_collection.delete_one({"username": username})
