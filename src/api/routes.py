"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException

from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import json

api = Blueprint('api', __name__)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

#from models import Person






# Setup the Flask-JWT-Extended extension
api.config["JWT_SECRET_KEY"] = "top-secret"  # Change this! estaba super-secret y lo cambié por top-secret
jwt = JWTManager(api)

# Handle/serialize errors like a JSON object
@api.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code



# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)   
    if email != "test" or password != "test":
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@api.route('/signup', methods=['POST'])
def create_one_user():
    body = json.loads(request.data)
    new_user = User(
        email=body["email"],
        password=body["password"],
        is_active=True
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "user created succesfull"}), 200







#FINAL DEL CÓDIGO

# this only runs if `$ python src/main.py` is executed
# if __name__ == '__main__':
#     PORT = int(os.environ.get('PORT', 3001))
#     api.run(host='0.0.0.0', port=PORT, debug=True)
