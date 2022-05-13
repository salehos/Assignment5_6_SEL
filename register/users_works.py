from pymongo import MongoClient
import os
mongo_servers=str(os.environ.get('MONGO_SERVERS'))
mongo_client = MongoClient(mongo_servers)

database = mongo_client.get_database(name="bidood")
user_col = database.get_collection(name="users")

def check_user_exist(username, gmail):
    username_check = user_col.find_one({"username": username})
    gmail_check = user_col.find_one({"gmail": gmail})
    if username_check != None:
        if gmail_check != None:
            return {"res" : "username and gmail are already picked"}
        return {"res" : "this username is already picked"}
    if gmail_check != None:
        return {"res" : "this gmail is already picked"}
    return None

def create_user(username, gmail, password):
    try :
        res = user_col.insert_one({
            "username" : username,
            "gmail": gmail,
            "password": password,
            "x": 0,
            "y": 0,
            "total_score": 0
        })
        return {'res': 'user created'}
    except Exception as e:
        return {
            "res" : "user can not be created",
            "error": str(e)
        }

# print(check_user_exist("abbass", "abbasi"))
