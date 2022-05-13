from pymongo import MongoClient
import os
mongo_servers=str(os.environ.get('MONGO_SERVERS'))
mongo_client = MongoClient(mongo_servers)

database = mongo_client.get_database(name="bidood")
travel_col = database.get_collection(name="travel")


def get_travel(travel_id):
    travel = travel_col.find_one({"travel_id": travel_id})
    if travel == None:
        return {'res' : 'there is no travel with this travel id'}
    return travel

def create_travel():
    pass

def end_travel(x, y, travel_id):
    pass

def get_all_travels(username):
    travels = travel_col.find({"rider_username": username})
    try:
        travels = list(travels)
    except:
        travels = None
    if travels == None:
        return {'res' : 'there is no travel with this travel id'}
    return travels
