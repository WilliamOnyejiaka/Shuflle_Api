from . import db
from typing import Dict, List
from datetime import datetime
from bson.objectid import ObjectId
from src.modules.Serializer import SerializeData


class Shuffle:

    @staticmethod
    def insert(data: Dict) -> bool:
        query_response = db.insert_one({
            'ip_address': data['ip_address'],
            'text': data['text'],
            'latest_shuffle': data['shuffled_text'],
            'number_of_shuffles': 1,
            'previous_shuffles':[data['shuffled_text']],
            'created_at': datetime.now(),
            'updated_at': None
        })

        return True if query_response.inserted_id else False

    @staticmethod
    def get_data(ip_address: str, text: str, needed_attr: List = [
        '_id',
        'ip_address',
        'text',
        'latest_shuffle',
        'number_of_shuffles',
        'previous_shuffles',
        'created_at',
        'updated_at'
    ]):
        query_response = db.find_one(
            {'ip_address': ip_address, 'text': text})
        if not query_response:
            return None
        else:
            return SerializeData(needed_attr).serialize(query_response)

    @staticmethod
    def update_data(ip_address:str,text:str,data: Dict):
        query_response = db.update_one({
            'ip_address':ip_address,
            'text':text
        }, {'$set': {
            'number_of_shuffles': data['number_of_shuffles'],
            'latest_shuffle':data['shuffled_text'],
            'previous_shuffles': data['previous_shuffles'],
            'updated_at': datetime.now()
        }})
        if query_response.modified_count > 0:
            return True
        else:
            return False
