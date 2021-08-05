from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import pymongo
import db_config as database # Establishes database
from bson.json_util import dumps, ObjectId # Dumps same as JSONIFY

app = Flask(__name__)
api = Api(app) # Creates the instance for the API

class Animal(Resource):
    """ Animals' actions """
    def post(self): # Creates an instance of the class READY AND WORKING
        _id = str(database.db.animals.insert_one({
            "name": request.json["name"], # request.json gets data we will add
            "type": request.json["type"],
            "food": request.json["food"],
            "environment": request.json["environment"]
        }).inserted_id)# Function to insert smn in the DB

        return "Your animal was added to the Zoo !" # Message that will appear once the process is done READY AND WORKING

    def get(self, by, data): # Gets the information of an animal
        response = self.abort_if_not_exist(by, data) # Do not do this def if id is not existent
        response['_id'] = str(response['_id'])

        return jsonify(response)


    def put(self, by, data): # Edits the information of an animal READY AND WORKING
        response = self.abort_if_not_exist(by, data) # Check if it exists before updating

        for key, value in request.json.items(): # Looks for elements inside json request
            response[key] = value

        database.db.animals.update_one({'_id': ObjectId(response['_id'])}, # Receives id to edit
            {'$set':{ # Looks for the element before editing it
                'name': response['name'],
                'type': response['type'],
                'food': response['food'],
                'environment': response['environment']
                }
            }
        )

        response['_id'] = str(response['_id'])
        return jsonify(response)

    def delete(self, by, data): # Transfers an animal from the zoo (removes it) READY AND WORKING
        response = self.abort_if_not_exist(by, data)
        database.db.animals.delete_one({'_id':response['_id']})
        response['_id'] = str(response['_id'])
        return jsonify({"deleted":response})

    def abort_if_not_exist(self, by, data): # Aborts an operation if the id doesn't exist
        if by == "_id":
            response = database.db.animals.find_one({"_id": ObjectId(data)}) # Returns id
        else:
            response = database.db.animals.find_one({f'{by}': data}) # Looks for any element (specified in by) in db

        if response: # If there is a response just return it
            return response
        else: # If not, send 404 error
            abort(jsonify({"status":404, f"{by}":f"{data} not found"}))

class AllAnimals(Resource): # OPTIONAL
    """ Gets all animals from Zoo """

    def get(self): # Gets a list of all animals in zoo
        response = list(database.db.animals.find())

        for doc in response:
            doc['_id'] = str(doc['_id'])

        return jsonify(response)

api.add_resource(Animal, '/new', '/<string:by>:<string:data>/') # Especifies url to access certain functions
api.add_resource(AllAnimals, '/all/')

if __name__ == '__main__': # Runs everything
    app.run(load_dotenv=True) # Gets info from .env file
