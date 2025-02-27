from flask import Blueprint, jsonify, request
from services.process_flavors import extract_flavors

route_flavors = Blueprint('flavors', __name__)

@route_flavors.route('/get_flavors', methods=['POST']) # type: ignore
def get_flavors():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        flavors = extract_flavors(file)
                    
        return jsonify(flavors)