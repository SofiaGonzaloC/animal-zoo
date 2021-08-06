from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import pymongo
import db_config as database
from bson.json_util import ObjectId

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

    def get(self, by, data):
        response = self.abort_if_not_exist(by, data)
        response['_id'] = str(response['_id'])

        return jsonify(response)

    def put(self, by, data):
        response = self.abort_if_not_exist(by, data)

        for key, value in request.json.items():
            response[key] = value

        database.db.animals.update_one({'_id': ObjectId(response['_id'])},
            { '$set': {
                "name": response["name"],
                "type": response["type"],
                "food": response["food"],
                "environment": response["environment"],
                }
            }
        )

        response['_id'] = str(response['_id'])
        return jsonify(response)

    def delete(self, by, data):
        response = self.abort_if_not_exist(by, data)
        database.db.animals.delete_one({'_id': response['_id']})
        response['_id'] = str(response['_id'])
        return "Animal was successfully transferred"

    def abort_if_not_exist(self, by, data):
        if by == "_id":
            response = database.db.animals.find_one({"_id": ObjectId(data)})
        else:
            response = database.db.animals.find_one({f'{by}': data})

        if response:
            return response
        else:
            abort(jsonify({"status": 404, f"{by}": f"{data} not found"}))

class AllAnimals(Resource):
    def get(self):
        response = list(database.db.animals.find())

        for doc in response:
            doc['_id'] = str(doc['_id'])

        return jsonify(response)

api.add_resource(Animal, '/new/', '/<string:by>:<string:data>/')
api.add_resource(AllAnimals, '/all/')

if __name__ == '__main__':
    app.run(load_dotenv=True)