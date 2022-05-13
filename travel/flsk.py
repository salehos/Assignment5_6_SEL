import os
from travel_stuff import get_travel, get_all_travels, create_travel, end_travel
from flask import Flask, request
app = Flask(__name__)

@app.route('/travel/get', methods=['POST'])
def get_travel():
    travel_data = {}
    try:
        if request.method == "POST":
            for m in request.form:
                travel_data.update({m : request.form[m]})
            travel = get_travel(travel_data['travel_id'])
            if travel != None:
                return travel
            else:
                return {'res': travel}
    except Exception as e:
        return {
                'res' : 'failed',
                'error' : str(e)
        }

@app.route('/travel/get_all', methods=['POST'])
def get_all_travel():
    travel_data = {}
    try:
        if request.method == "POST":
            for m in request.form:
                travel_data.update({m : request.form[m]})
            travel = get_all_travels(travel_data['username'])
            if travel == None:
                return travel
            else:
                return {'res': travel}
    except Exception as e:
        return {
                'res' : 'failed',
                'error' : str(e)
        }
    
@app.route('/travel/create_travel', methods=['POST'])
def c_t():
    travel_data = {}
    try:
        if request.method == "POST":
            for m in request.form:
                travel_data.update({m : request.form[m]})
            travel = create_travel(travel_data['username'], travel_data['bike_id'])
            if travel == None:
                return travel
            else:
                return {'res': travel}
    except Exception as e:
        return {
                'res' : 'failed',
                'error' : str(e)
        }

@app.route('/travel/end_travel', methods=['POST'])
def e_t():
    travel_data = {}
    try:
        if request.method == "POST":
            for m in request.form:
                travel_data.update({m : request.form[m]})
            travel = end_travel(travel_data['username'], travel_data['travel_id'], travel_data['x'], travel_data['y'])
            return travel
    except Exception as e:
        return {
                'res' : 'failed',
                'error' : str(e)
        }

if __name__ == '__main__':
   app.run(debug = True, port= 1234)