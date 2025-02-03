from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from bson import json_util, ObjectId


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/pythonMongodb"
mongo = PyMongo(app)

@app.route('/users', methods=["POST"])
def create_user():
    username = request.json["name"]
    password = request.json["password"]
    email = request.json["email"]
    
    hashedPassword = generate_password_hash(password)
    print(hashedPassword)
    
    if username and email and password:
        id = mongo.db.users.insert_one(
            {
                "username": username,
                "password": hashedPassword,
                "email": email
            }
        )
        
        splitid = str(id).split("(") 
        idN = splitid[2]
        id_result = idN.split(")")[0]
        print(id_result)

        response = {
                "id": id_result,
                "username": username,
                "password": hashedPassword,
                "email": email
    }
        
        return response
    else:
        return not_found()

@app.route("/users", methods=["GET"])
def getAllUsers():
    users = mongo.db.users.find({"username": "camilo"})
    response = json_util.dumps(users)
    
    return Response(response, mimetype='aplication/json')

@app.route("/users/<string:_id>", methods=["GET"])
def getUser(_id):
    objInstance = ObjectId(_id)
    user = mongo.db.users.find_one({"_id": objInstance })
    print(user)
    response = json_util.dumps(user)
    print(response)
    return Response(response, mimetype="application/json")

@app.route("/users/<string:_id>", methods=["DELETE"])
def deleteUser(_id):
    objInstance = ObjectId(_id)
    user = mongo.db.users.delete_one({"_id": objInstance })
    response = jsonify({"message": "User eliminado" + id})
    
    return response

@app.route('/users/<id>', methods=["PUT"])
def update_user(id):
    username = request.json['username']
    password = request.json['password']
    email = request.json["email"]
    
    if username and password and email and id:
        hashed_password = generate_password_hash(password)
        
        mongo.db.users.update_one({'_id': ObjectId(id)},
        {'$set':{
            'username': username,
            'password': hashed_password,
            'email': email
        }})        
        
        return jsonify({'message': 'User ' + id + ' updated successfully'}), 200
    else:
        return jsonify({'message': 'Missing fields'}), 400


# @app.route("/users/id", methods="POST")

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource not Found: ' + request.url,
        'status': 404
    }
    return jsonify(message), 404

if __name__ == '__main__':
    app.run(debug=True)