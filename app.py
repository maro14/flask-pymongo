from flask import Flask, Response, request, jsonify
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/user.user"
mongo = PyMongo(app)



@app.route("/", methods=["GET"])
def index():
	return "Pymmongo"



@app.route("/users", methods=["GET"])
def get_name():
	users = mongo.db.users.find()
	response = json_util.dumps(users)
	return Response(response, mimetype="application/json")


@app.route("/users/<id>", methods=["GET"])
def get_user(id):
	user = mongo.db.users.find_one_or_404({'_id', ObjectId(id), })
	response = json_util.dumps(user)
	return Response(response, mimetype="application/json")


@app.route("/name", methods=["POST"])
def add_name():
	name = request.json['name']

	id = mongo.db.users.insert({
		'name': name
		})
	response = jsonify({
		'name' : name
		})
	response.status_code = 201
	return response



@app.route('/name/<_id>', methods=['PUT'])
def update_name(_id):
    name = request.json['name']

    _id = mongo.db.users.update_one(
        {'_id': ObjectId(_id['$oid']) if '$iod' in _id else ObjectId(_id)},
        {'$set': {'name': name}})
    response = jsonify({'massage': 'User' + _id + 'Updated'})
    response.status_code = 200
    return response



@app.errorhandler(404)
def not_found(error=None):
	message = {
		'message': 'Resource Not Found ' + request.url,
        'status': 404
	}
	response = jsonify(message)
	response.status_code = 404
	return response



if __name__ == "__main__":
	app.run(debug=True, port=8080)