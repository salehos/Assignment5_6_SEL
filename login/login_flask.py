from flask import Flask, request

from login_works import check_user_credential, encode_auth_token

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login_user():
    user_data = {}
    try:
        for m in request.form:
            user_data.update({m: request.form[m]})
        check_user = check_user_credential(user_data['username'], user_data['password'])
        if check_user is not None:
            return check_user
        else:
            return {"res": "Login was successful", "token": encode_auth_token(user_data['username'])}
    except Exception as e:
        return {
            'res': 'failed',
            'error': str(e)
        }


if __name__ == '__main__':
    app.run(debug=True)
