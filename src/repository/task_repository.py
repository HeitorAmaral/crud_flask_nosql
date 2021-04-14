"""
Database communication
"""
import os
from flask_pymongo import PyMongo

mongo = None


class TaskRepository:
    """
    Class to communicate with Database and make operations.
    """
    def __init__(self, app):
        self.app = app

    def get_mongo_connection(self):
        """
        Method to initialize the MongoDB connection.
        :return: Mongodb connection instance.
        :rtype: PyMongo
        """
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
        """
        Method to do a query in the database. Can be used parameters
         to filter results, and fields to restrict return properties.
        :param parameters: Constraints, or empty for all.
        :type parameters: dict
        :param fields: Fields required or empty for all.
        :type fields: dict
        :return: Query result containing all the documents queried.
        :rtype: pymongo.cursor.Cursor
        """
        return self.get_mongo_connection().db.task.find(parameters, fields)

    def find_one(self, parameters):
        """
        Method to do a query in the database. Can be used parameters
         to filter results.
        :param parameters: Constraints, or empty for all.
        :type parameters: dict
        :return: Query result containing the document queried.
        :rtype: dict
        """
        return self.get_mongo_connection().db.task.find_one(parameters)

    def insert_one(self, task_id, description, status):
        """
        Method to insert a object in the database.
        :param task_id: Identifier of the Task.
        :type task_id: int
        :param description: Description of the Task.
        :type description: str
        :param status: Status of the Task (Finished or No).
        :type status: bool
        :return: Instance of InsertOneResult, containing information
         about insert operation.
        :rtype: pymongo.results.InsertOneResult
        """
        return self.get_mongo_connection()\
            .db.task.insert_one({"_id": task_id,
                                 "description": description,
                                 "status": status})

    def update_one(self, parameters, new_data):
        """
        Method to update a object in the database.
        :param parameters: Constraints of the object to be updated
         (Like Identifier)
        :type parameters: dict
        :param new_data: New data to be placed in the object.
        :type new_data: dict
        :return: Instance of UpdateResult, containing information about
         update operation.
        :rtype: pymongo.results.UpdateResult
        """
        return self.get_mongo_connection()\
            .db.task.update_one(parameters, {"$set": new_data})

    def delete_one(self, parameters):
        """
        Method to delete a object in the database.
        :param parameters: Constraints of the object to be deleted
         (Like Identifier)
        :type parameters: dict
        :return: Instance of DeleteResult, containing information about
         delete operation.
        :rtype: pymongo.results.DeleteResult
        """
        return self.get_mongo_connection().db.task.delete_one(parameters)
