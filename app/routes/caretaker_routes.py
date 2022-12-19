from app import db
from app.models.caretaker import Caretaker
from app.models.dog import Dog
from app.routes.routes_helper import *
from flask import Blueprint, jsonify, abort, make_response, request

caretaker_bp = Blueprint("caretaker_bp", __name__, url_prefix="/caretakers")

@caretaker_bp.route("", methods=["POST"])
def create_caretaker():
    request_body = request.get_json()
    new_caretaker = Caretaker.from_dict(request_body)

    db.session.add(new_caretaker)
    db.session.commit()

    return make_response(jsonify(f"Caretaker {new_caretaker.name} successfully created"), 201)

@caretaker_bp.route("", methods=["GET"])
def read_all_caretaker():
    caretakers = Caretaker.query.all()
    caretaker_response = [caretaker.to_dict() for caretaker in caretakers]
    return jsonify(caretaker_response)

# NESTED ROUTES
@caretaker_bp.route("/<id>/dogs", methods=["POST"])
def create_dog(id):
    request_body = request.get_json()
    caretaker = get_record_by_id(Dog, id)

    new_dog = Dog.from_dict(request_body)
    new_dog.caretaker = caretaker
    
    db.session.add(new_dog)
    db.session.commit()

    return make_response(jsonify(f"Dog {new_dog.name} cared by {caretaker.name} successfully created"), 201)


@caretaker_bp.route("/<id>/dogs", methods=["GET"])
def read_dogs_of_caretaker(id):
    caretaker = get_record_by_id(Dog, id)
    dog_response = [dog.to_dict() for dog in caretaker.dogs]

    return(jsonify(dog_response))