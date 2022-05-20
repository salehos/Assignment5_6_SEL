from flask import Flask, request

from travel_stuff import get_travel_details, get_all_travels, create_travel, end_travel

app = Flask(__name__)


@app.route('/travel/get', methods=['POST'])
def get_travel():
    travel_data = {}
    try:
        if request.method == "POST":
            for m in request.form:
                travel_data.update({m: request.form[m]})
            try:
                travel_id = travel_data['travel_id']
            except Exception as e:
                return {'res': 'there is no travel_id in your body'}
            travel = get_travel_details(travel_id=travel_id)
            if travel != None:
                return travel
            else:
                return {'res': travel}
    except Exception as e:
        return {
            'res': 'failed',
            'error': str(e)
        }


@app.route('/travel/get_all', methods=['POST'])
def get_all_travel():
    travel_data = {}
    try:
        if request.method == "POST":
            for m in request.form:
                travel_data.update({m: request.form[m]})
            try:
                username = travel_data['username']
            except Exception as e:
                return {'res': 'there is no username in your body'}
            travel = get_all_travels(username=username)
            if travel == None:
                return travel
            else:
                return {'res': travel}
    except Exception as e:
        return {
            'res': 'failed',
            'error': str(e)
        }


@app.route('/travel/create_travel', methods=['POST'])
def c_t():
    travel_data = {}
    try:
        if request.method == "POST":
            for m in request.form:
                travel_data.update({m: request.form[m]})
            try:
                username, bike_id, x, y = travel_data['username'], travel_data['bike_id'], travel_data['x'], \
                                          travel_data['y']
            except Exception as e:
                return {'res': 'there is no username or bike_id or x or y in your body'}
            travel = create_travel(username, bike_id, x, y)
            if travel == None:
                return travel
            else:
                return {'res': travel}
    except Exception as e:
        return {
            'res': 'failed',
            'error': str(e)
        }


@app.route('/travel/end_travel', methods=['POST'])
def e_t():
    travel_data = {}
    try:
        if request.method == "POST":
            for m in request.form:
                travel_data.update({m: request.form[m]})
            try:
                username, travel_id, x, y = travel_data['username'], travel_data['travel_id'], travel_data['x'], \
                                            travel_data['y']
            except Exception as e:
                return {'res': 'there is no username or bike_id or x or y in your body'}
            travel = end_travel(username, travel_id, x, y)
            return travel
    except Exception as e:
        return {
            'res': 'failed',
            'error': str(e)
        }


if __name__ == '__main__':
    app.run(debug=True, port=1234)
