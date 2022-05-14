import os
from flask import Flask, request
from users_works import check_user_exist, create_user
app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    user_data = {}
    try:
        if request.method == "POST":
            for m in request.form:
                user_data.update({m : request.form[m]})
            check_user = check_user_exist(user_data['username'], user_data['gmail'])
            if check_user != None:
                return check_user
            else:
                return create_user(user_data['username'], user_data['gmail'], user_data['password'])
    except Exception as e:
        return {
                'res' : 'failed',
                'error' : str(e)
        }
    

if __name__ == '__main__':
   app.run(debug = True, port= 3456)