import os
from flask_pymongo import PyMongo

mongo = None


class TaskRepository:

    def __init__(self, app):
        self.app = app

    def get_mongo_connection(self):
        global mongo

        if 'MONGO_URI' not in self.app.config:
            self.app.config['MONGO_URI'] = "mongodb://"\
                          + os.environ['MONGODB_USERNAME']\
                          + ":" + os.environ['MONGODB_PASSWORD']\
                          + "@" + os.environ['MONGODB_HOSTNAME']\
                          + "/" + os.environ['MONGODB_DATABASE']

        if not mongo:
            mongo = PyMongo(self.app)

        return mongo

    def find(self, parameters, fields):
        return self.get_mongo_connection().db.task.find(parameters,
                                                        fields)

    def find_one(self, parameters):
        return self.get_mongo_connection().db.task.find_one(parameters)

    def insert_one(self, task_id, description, status):
        return\
            self.get_mongo_connection()\
                .db.task.insert_one({"_id": task_id,
                                     "description": description,
                                     "status": status})

    def update_one(self, parameters, new_data):
        return\
            self.get_mongo_connection()\
                .db.task.update_one(parameters, {"$set": new_data})

    def delete_one(self, parameters):
        return\
            self.get_mongo_connection()\
                .db.task.delete_one(parameters)
