from flask import Flask, Response, request, jsonify
from flask_pymongo import PyMongo
from bson import json_util


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/user.user"
mongo = PyMongo(app)



@app.route("/user", methods=["GET"])
def get_all_users():
	users = mongo.db.users.find()
	response = json_util.dumps(users)
	return Response(response, mimetype="application/json")



@app.route("/user", methods=["POST"])
def add_user():
	name = request.json['name']

	id = mongo.db.users.insert({
		'name': name
		})
	response = jsonify({
		'name' : name
		})
	response.status_code = 201
	return response

@app.route('/user/<_id>', methods=['PUT'])
def update_user(_id):
    name = request.json['name']
    age = request.json['age']

    mongo.db.user.update_one(
    {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': name, 'age': age}})
    response = jsonify({'messsage': 'User'+ _id +'updated'})
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
