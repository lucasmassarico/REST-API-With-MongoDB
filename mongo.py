from flask_pymongo import PyMongo

banco = PyMongo()


class Database:
    def __init__(self, app):
        self.app = app

    def initialize(self):
        client = PyMongo()
        client.init_app(self.app)
        return client.db

