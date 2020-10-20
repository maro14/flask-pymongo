from flask import Flask, Response, request, jsonify
from flask_pymongo import PyMongo
from bson import json_util


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/user.user"
mongo = PyMongo(app)



@app.route("/", methods=["GET"])
def index():
	return "Hello World"



@app.route("/name", methods=["GET"])
def get_name():
	users = mongo.db.users.find()
	response = json_util.dumps(users)
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
