from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import LOGGER

uri = os.environ['MONGODB_URI']
client = MongoClient(uri, server_api=ServerApi('1'))
USERS = client['UserInfo']
user_coll = USERS['UserInfo']

def doesUserExist(username: str) -> bool:
    user_document = user_coll.find_one({"username": username})
    if user_document: return True
    else: return False   
    
