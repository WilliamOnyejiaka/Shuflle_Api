from . import db
from typing import Dict, List
from datetime import datetime
from bson.objectid import ObjectId
from src.modules.Serializer import SerializeData


class Shuffle:

    @staticmethod
    def insert(data: Dict) -> bool:
        current_shuffle = {
            'shuffled_text':data['shuffled_text'],
            'shuffled_at':datetime.now()
        }
        query_response = db.insert_one({
            'ip_address': data['ip_address'],
            'text': data['text'],
            'latest_shuffle': data['shuffled_text'],
            'number_of_shuffles': 1,
            'previous_shuffles':[current_shuffle],
            'created_at': datetime.now(),
            'updated_at': None
        })

        return True if query_response.inserted_id else False
    
    @staticmethod
    def find_item(item:Dict, needed_attr: List = [
        '_id',
        'ip_address',
        'text',
        'latest_shuffle',
        'number_of_shuffles',
        'previous_shuffles',
        'created_at',
        'updated_at'
    ]):
        query_response = db.find_one(item)
        return SerializeData(needed_attr).serialize(query_response) if query_response else None

    @staticmethod
    def get_data(ip_address: str, text: str, needed_attr:List=None):
        if needed_attr:
            return Shuffle.find_item({'ip_address': ip_address, 'text': text}, needed_attr)
        else:
            return Shuffle.find_item({'ip_address': ip_address, 'text': text})

        # query_response = db.find_one(
        #     {'ip_address': ip_address, 'text': text})
        # if not query_response:
        #     return None
        # else:
        #     return SerializeData(needed_attr).serialize(query_response)
    
    @staticmethod
    def get_data_with_id_and_addr(id:str,ip_address:str,needed_attr:List=None):
        if needed_attr:
            return Shuffle.find_item({'_id': ObjectId(id), 'ip_address': ip_address}, needed_attr)
        else:
            return Shuffle.find_item({'_id': ObjectId(id), 'ip_address': ip_address})

    @staticmethod
    def get_user_data(ip_address:str,needed_attr=[
        '_id',
        'ip_address',
        'text',
        'latest_shuffle',
        'number_of_shuffles',
        'previous_shuffles',
        'created_at',
        'updated_at'
    ]):
        query_response = db.find({'ip_address':ip_address}).sort('_id')
        return SerializeData(needed_attr).dump(list(query_response)) if query_response else []

    @staticmethod
    def update_data(previous_data: Dict,shuffled_text: str):
        current_shuffle = {
            'shuffled_text': shuffled_text,
            'shuffled_at': datetime.now()
        }

        previous_data['previous_shuffles'].append(current_shuffle)
        number_of_shuffles = int(previous_data['number_of_shuffles']) + 1

        query_response = db.update_one({
            'ip_address': previous_data['ip_address'],
            'text': previous_data['text']
        }, {'$set': {
            'number_of_shuffles': number_of_shuffles,
            'latest_shuffle': shuffled_text,
            'previous_shuffles': previous_data['previous_shuffles'],
            'updated_at': datetime.now()
        }})
        if query_response.modified_count > 0:
            return True
        else:
            return False

    @staticmethod
    def search(ip_address:str, search_string: str,needed_attr=[
        '_id',
        'ip_address',
        'text',
        'latest_shuffle',
        'number_of_shuffles',
        'previous_shuffles',
        'created_at',
        'updated_at'
    ]):
        query = db.find({'ip_address': ip_address, 'text': {
            '$regex': search_string,
            "$options": 'i'
        }}).sort('_id')

        return SerializeData(needed_attr).dump(list(query)) if query else []

    @staticmethod
    def delete_one(ip_address:str,id:str):
        query_response = db.delete_one({'_id':ObjectId(id),'ip_address':ip_address})
        return query_response.deleted_count > 0