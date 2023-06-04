#!/usr/bin/python3
"""This file will contain will handle default RESTful API actions"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """retrieves a list of all states"""
    states = storage.all("State")
    my_states = [value.to_dict() for key, value in states.items()]
    return jsonify(my_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_states(state_id):
    """Delete specific state based on its id"""

    my_state = storage.get(State, state_id)
    if my_state is not None:
        storage.delete(my_state)
        storage.save()
        return (jsonify({}))
    else:
        abort(404)

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_states():
    """It provides new information to the server"""

    content = reqest.get_json()
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    name = content.get("name")
    if name is None:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**content)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_states(state_id):
    """Update a state"""

    content = request.get_json()
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400

    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)

    not_allowed = ["id", "created_at", "updated_at"]
    for key, value in content.items():
        if key not in not_allowed:
            setattr(my_state.__class__, key, value)

    my_state.save()
    return jsonify(my_state.to_dict())
