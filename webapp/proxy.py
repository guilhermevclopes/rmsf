from flask import Flask
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify, url_for
from flask import session as flasksession
from flask import abort
import requests
import os

import database
from sqlalchemy.sql.sqltypes import JSON

app = Flask(__name__)
app.secret_key = "espelhoMeu"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


# JSON
# [
#     {
#         username: Gui
#         password: pass
#     }
# ]

@app.route('/')
def home_page():
    return render_template("home.html")

# @app.route('/Auth/signup', methods = ['POST'])
# def signup():
#     try:
#         database.new_user(request.get_json())
#     except:
#         return 0
#     return 1

# @app.route('/Auth/login', methods=['POST'])
# def login():
#     try:
#         database.check_login(request.get_json())
#     except:
#         return 0
#     return 1

# @app.route('/Settings/fetch/<str:user>', methods = ['GET'])
# def fetch_settings(user):
#     try:
#         settings = database.get_settings(user)
#     except:
#         abort(400)
#     return settings

# @app.route('/Settings/update/<str:user>', methods = ['POST'])
# def update_settings(user):
#     try:
#         settings = database.update_settings(user, request.get_json())
#     except:
#         return 0
#     return 1


# @app.route('/Pictures/upload/<str:user>', methods = ['POST'])
# def upload_pictures(user):
#     return

if __name__ == '__main__':
    app.run(port=5000,debug=True)
   