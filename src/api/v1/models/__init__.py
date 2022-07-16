from pymongo import MongoClient
from src.config import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client.shuffle_api_db.db