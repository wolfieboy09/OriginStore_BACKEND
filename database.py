from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import LOGGER
from bson import ObjectId

uri = os.environ['MONGODB_URI']
client = MongoClient(uri, server_api=ServerApi('1'))

def doesUserExist(username: str) -> bool:
    user_coll = client.get_database()['OSLapps']
    user_document = user_coll.find_one({"username": username})
    if user_document: return True
    else: return False   
    
    
def newApp(name: str, author: str, current_ver: float, description: str, author_link_types: list, links: list, required_ver: float, download_file: str) -> bool:
    app_coll = client.get_database()['OSLapps']
    INSERT = {
        "_id": ObjectId(),
        "name": name,
        "author": author,
        "current_var": f"{current_ver}",
        "description": description,
        "author_link_types": f"{author_link_types}",
        "required_ver": f"{required_ver}",
        "links": f"{links}",
        "download_file": f"{download_file}"
        }
    app_coll.insert_one(INSERT)
    return True


def getAllApps():
    collection = client.get_database()['OSLapps']
    result = collection.find({}, {'_id': 1, 'name': 1, 'author': 1, 'current_var': 1, 'description': 1, 'author_link_types': 1, 'links': 1, 'required_ver': 1, 'download_file': 1})
    apps_list = []
    for document in result:
        apps_list.append(document)
    response_json = {"apps": apps_list}
    return response_json

   

        
    
