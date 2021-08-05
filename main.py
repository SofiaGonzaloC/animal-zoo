from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import pymongo
import db_config as database # Establishes database

app = Flask(__name__)
api = Api(app) # Creates the instance for the API

class Animal(Resource):
    def post(self): # Creates an instance of the class
        _id = database.db.animals.insert_one({
            "name": request.json["name"], # request.json gets data we will add
            "type": request.json["type"],
            "food": request.json["food"],
            "environment": request.json["environment"]
        }) # Function to insert smn in the DB

        return "Your animal was added to the Zoo !" # Message that will appear once the process is done

class AllAnimals(Resource): 
    """ Gets all animals from Zoo """
    def get(self):
        pass

api.add_resource(Animal, '/new') # Especifies url to access certain functions

if __name__ == '__main__':
    app.run(load_dotenv=True) # Gets info from .env file
