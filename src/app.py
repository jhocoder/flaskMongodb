from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash


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
        return jsonify({"message": "ruta users"})


@app.errorhandler(404)
def not_found(error=None):
     message = {
            'message': 'Resource not Found' + request.url,
            'satus': 404
    }

if __name__ == '__main__':
    app.run(debug=True)