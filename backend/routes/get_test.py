from flask import Blueprint, jsonify, send_from_directory
import os

route_test = Blueprint('test', __name__)

@route_test.route('/render', methods=['GET']) # type: ignore
def get_flavors():
    return jsonify(message="This is a test message")