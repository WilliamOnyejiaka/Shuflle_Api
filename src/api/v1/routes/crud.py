import json
from flask import Blueprint, jsonify, request
from src.modules.validate_ip_address import validate_ip_address
from src.modules.PyShuffle import PyShuffle
from src.api.v1.models.Shuffle import Shuffle
from datetime import datetime

crud = Blueprint('crud', __name__, url_prefix='/api/v1/shuffle')


@crud.post('/<text>')
def shuffle(text: str):
    ip_address = request.environ.get(
        'HTTP_X_FORWARDED_FOR', request.remote_addr)
    valid_address = validate_ip_address(ip_address)

    if valid_address:
        user = Shuffle.get_data(ip_address, text)
        shuffled_text = PyShuffle(text).shuffle()
        if user:
            user['previous_shuffles'].append(shuffled_text)
            previous_shuffles = user['previous_shuffles']
            data = {
                'shuffled_text': shuffled_text,
                'number_of_shuffles': user['number_of_shuffles']+1,
                'previous_shuffles': previous_shuffles
            }

            if Shuffle.update_data(ip_address, text,data):
                return jsonify({'error': False, 'shuffled_text': shuffled_text}),200
            return jsonify({'error':True,'message':"something went wrong"}),500
        
        data = {
            'ip_address': ip_address,
            'text': text,
            'shuffled_text': shuffled_text
        }

        if Shuffle.insert(data):
            return jsonify({'error': False, 'shuffled_text': shuffled_text}), 200
        return jsonify({'error': True, 'message': "something went wrong"}), 500

    return jsonify({'error': True, 'message': 'invalid ip address'}), 400
