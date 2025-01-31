from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/pythonMongodb"
mongo = PyMongo(app)

@app.route('/users', methods=["POST"])
def create_user():
    print(request.get_json)
    return jsonify({"message": "ruta users"})



if __name__ == '__main__':
    app.run(debug=True)