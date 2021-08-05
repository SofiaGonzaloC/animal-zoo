from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import pymongo
import db_config as database
# from bson.json_util import Dumps, ObjectId

app = Flask(__name__)
api = Api(app)

class Animal(Resource):
    def post(self):
        _id = str(database.db.animals.insert_one({
            "name": request.json["name"],
            "type": request.json["type"],
            "food": request.json["food"],
            "environment": request.json["environment"],
        }).inserted_id)

        return "Your animal was added to the Zoo !"

class AllAnimals(Resource):
    def get(self):
        response = list(database.db.animals.find())

        for doc in response:
            doc['_id'] = str(doc['_id'])

        return jsonify(response)

api.add_resource(Animal, '/new/')
api.add_resource(AllAnimals, '/all/')

if __name__ == '__main__':
    app.run(load_dotenv=True)