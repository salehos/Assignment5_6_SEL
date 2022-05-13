import requests
from flask import Flask, request, Response

from main_works import auth_decorator

app = Flask(__name__)


@app.route('/main/<route>')
@auth_decorator
def main(route):
    try:
        request_method = request.method
        host = "127.0.0.1"
        port = 8000
        response = requests.request(method=request_method,
                                    url=f"{host}:{port}/{route}",
                                    params=request.args,
                                    headers={key: value for (key, value) in request.headers if key != 'Host'},
                                    data=request.get_data(),
                                    cookies=request.cookies,
                                    allow_redirects=False,
                                    stream=True
                                    )
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in response.raw.headers.items()
                   if name.lower() not in excluded_headers]
        return Response(response.content, response.status_code, headers)
    except Exception as e:
        print(e)
        return {"res": str(e)}


if __name__ == '__main__':
    app.run(debug=True)
