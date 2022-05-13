from pymongo import MongoClient
import os
from uuid import uuid1
from datetime import datetime
mongo_servers=str(os.environ.get('MONGO_SERVERS'))
mongo_client = MongoClient(mongo_servers)

database = mongo_client.get_database(name="bidood")
travel_col = database.get_collection(name="travel")
user_col = database.get_collection(name="users")
bike_col = database.get_collection(name="bikes")


from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def get_travel_details(travel_id):
    travel = travel_col.find_one({"travel_id": travel_id})
    if travel == None:
        return {'res' : 'there is no travel with this travel id'}
    return travel

def create_travel(username, bike_id, x, y):
    is_ongoing = travel_col.find({"rider_username": username, "status": "Ongoing"})
    bike_json = bike_col.find_one({"bike_id": bike_id})
    user_json = user_col.find_one({"username": username})
    if is_ongoing != None:
        return {'res' : 'you have a travel ongoing! you cant create another'}
    if user_json == None:
        return {'res' : 'your username is WRONG'}
    if bike_json['status'] == 'busy':
        return {'res' : 'this bike is busy'}
    if haversine(bike_json['x'], bike_json['y'], x, y) > 100:
        return {'res' : 'bike is out of range'}
    travel_id = uuid1()
    travel_data = {
        "rider_username" : username,
        "travel_id" : travel_id,
        "x_start" : bike_json['x'],
        "y_start" : bike_json['x'],
        "bike_id" : bike_json['bike_id'],
        "x_end" : "",
        "y_end" : "",
        "distance" : "",
        "start_date" : str(datetime.now()),
        "end_date" : "",
        "status" : "Ongoing",
        "score" : 0
    }
    bike_updates = {
        "bike_id": bike_id,
        "x" : bike_json['x'],
        "y": bike_json['y'],
        "type": "busy",
    }
    bike_col.update_one(bike_json, {"$set": bike_updates})
    res = travel_col.insert_one(travel_data)
    return {'res': 'your travel has been created with id ' + str(travel_id)+ '. hold it for when you want to finish your move.'}

def end_travel(username, travel_id, x, y):
    travel_data_on_database = travel_col.find_one({'travel_id' : travel_id, 'status': 'Ongoing', 'rider_username': username})
    rider = user_col.find_one({"username": username})
    bike = bike_col.find_one({"bike_id": travel_data_on_database['bike_id']})
    all_travels = travel_col.find({"distance": { '$gt': 0 }})
    all_travels = list(all_travels)
    total_distance_of_all_users = 0
    for t in all_travels:
        total_distance_of_all_users += t['distance']
    total_distance_of_all_users = float(total_distance_of_all_users)/len(all_travels)
    if travel_data_on_database == None:
        return {'res': 'there is no travel with this id and username for rider, maybe it is not ongoing for now!'}
    distance = haversine(travel_data_on_database['x_start'],travel_data_on_database['y_start'],x,y)
    score = int(((distance)/total_distance_of_all_users)^2) +1
    travel_data = {
        "rider_username" : username,
        "travel_id" : travel_data_on_database['travel_id'],
        "x_start" : travel_data_on_database['x_start'],
        "y_start" : travel_data_on_database['y_start'],
        "bike_id" : travel_data_on_database['bike_id'],
        "x_end" : x,
        "y_end" : y,
        "distance" : distance,
        "start_date" : travel_data_on_database['start_date'],
        "end_date" : str(datetime.now()),
        "status" : "Finish",
        "score" : score
    }
    bike_data = {
        "bike_id": travel_data_on_database['bike_id'],
        "x" : x,
        "y": y,
        "type": "free",
    }
    user_data = {
        "username": rider['username'],
        "gmail": rider['gmail'] ,
        "password": rider['password'] ,
        "total_score": rider['total_score'] + score,
        "x": x,
        "y": y
    }
    bike_col.update_one(bike, {"$set": bike_data})
    user_col.update_one(rider, {"$set": user_data})
    travel_col.update_one(travel_data_on_database, {"$set": travel_data})
    return {'res': 'you finished your travel successfully, your score for this trip is '+ str(score)}


def get_all_travels(username):
    travels = travel_col.find({"rider_username": username})
    try:
        travels = list(travels)
    except:
        travels = None
    if travels == None:
        return {'res' : 'there is no travel with this travel id'}
    return travels
