import os

from pymongo import MongoClient

mongo_servers = str(os.environ.get('MONGO_SERVERS'))
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
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


def calculate_score(username, travel_id, x, y):
    travel_data_on_database = travel_col.find_one(
        {'travel_id': travel_id, 'status': 'Ongoing', 'rider_username': username})
    if travel_data_on_database is None:
        return {'res': 'there is no travel with this id and username for rider, maybe it is not ongoing for now!'}
    all_travels = travel_col.find({"distance": {'$gt': 0}})
    all_travels = list(all_travels)
    total_distance_of_all_users = 0
    for t in all_travels:
        total_distance_of_all_users += t['distance']
    total_distance_of_all_users = float(total_distance_of_all_users) / len(all_travels)

    distance = haversine(travel_data_on_database['x_start'], travel_data_on_database['y_start'], x, y)
    score = int(((distance) / total_distance_of_all_users) ^ 2) + 1
    travel_data = {
        "travel_id": travel_id,
        "score": score
    }

    travel_col.update_one(travel_data_on_database, {"$set": travel_data})
    return {'res': score}
