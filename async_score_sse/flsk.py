from flask import Flask
from flask import request
from flask_sse import sse

from travel_stuff import calculate_score

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/score')


@app.route('/score/calculate_travel_score', methods=['POST'])
def calculate_score_and_send_to_sse():
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
            score = calculate_score(username, travel_id, x, y)

            sse.publish(score, type='publish')
            return score
    except Exception as e:
        return {
            'res': 'failed',
            'error': str(e)
        }


if __name__ == '__main__':
    app.run(debug=True, port=1234)
