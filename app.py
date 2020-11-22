from flask import Flask, Response, request, jsonify
from flask_pymongo import PyMongo
from bson import json_util


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/user.user"
mongo = PyMongo(app)


@app.route('/username', methods=['POST'])
def post_username():
    name = request.json['name']
    age = request.json['age']

    id = mongo.db.user.insert_one({
        'name': name,
        'age': age
    })

    reponse = jsonify({
        '_id': str(id),
        'name': name,
        'age': age
    })
    response.status_code = 201
    return reponse

@app.route('/username', methods=['GET'])
def get_username():
    users = mongo.db.user.find()
    finish = json_util.dumps(users)
    return Response(finish, mimetype="application/json")

	

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
