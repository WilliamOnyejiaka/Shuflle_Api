from flask import Blueprint, jsonify, request
from src.modules.validate_ip_address import validate_ip_address
from src.modules.PyShuffle import PyShuffle
from src.api.v1.models.Shuffle import Shuffle
from datetime import datetime
from src.modules.Pagination import Pagination

crud = Blueprint('crud', __name__, url_prefix='/api/v1/shuffle')


@crud.post('/<text>')
def shuffle(text: str):
    ip_address = request.environ.get(
        'HTTP_X_FORWARDED_FOR', request.remote_addr)
    valid_address = validate_ip_address(ip_address)

    if valid_address:
        previous_data = Shuffle.get_data(ip_address, text)
        shuffled_text = PyShuffle(text).shuffle()
        if previous_data:
            if Shuffle.update_data(previous_data,shuffled_text):
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


@crud.get('/')
def get_user_shuffles():
    ip_address = request.environ.get(
        'HTTP_X_FORWARDED_FOR', request.remote_addr)

    user_data = Shuffle.get_user_data(ip_address)
    return jsonify({'error': False, 'data': user_data}), 200

@crud.get('/paginate')
def paginate():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit',10))
    except Exception:
        return jsonify({'error':True,'message':"page and limit values must be integers"}),400
    
    ip_address = request.environ.get(
        'HTTP_X_FORWARDED_FOR', request.remote_addr)

    user_data = Shuffle.get_user_data(ip_address)
    data = Pagination(user_data,page,limit).meta_data()

    return jsonify({'error':False,'data':data})

@crud.get('/search/<search_string>')
def search(search_string):
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except Exception:
        return jsonify({'error': True, 'message': "page and limit values must be integers"}), 400

    ip_address = request.environ.get(
        'HTTP_X_FORWARDED_FOR', request.remote_addr)

    data = Pagination(Shuffle.search(ip_address, search_string),page,limit).meta_data()
    
    return jsonify({'error':False,'data':data}),200

@crud.delete('/<id>')
def delete(id):
    ip_address = request.environ.get(
        'HTTP_X_FORWARDED_FOR', request.remote_addr)

    if Shuffle.get_data_with_id_and_addr(id, ip_address):
        if Shuffle.delete_one(ip_address,id):
            return jsonify({'error':False,'message':"item deleted"}),200
        return jsonify({'error':True,'message':"something went wrong"}),500

    return jsonify({'error':True,'message':"item not found"}),404
