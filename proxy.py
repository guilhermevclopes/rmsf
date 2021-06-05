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

current_user = ""

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

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/photos')
def photos():
    return render_template("photos.html")

@app.route('/settings')
def settings():
    return render_template("settings.html")

@app.route('/Auth/signup', methods = ['POST'])
def auth_signup():
    try:
        resp = database.new_user(request.get_json())
        print(resp)
        if resp:
            return redirect(url_for("login"))
        else:
            return redirect(url_for("home_page"))
    except:
            return redirect(url_for("home_page"))

@app.route('/Auth/login', methods=['POST'])
def auth_login():
    try:
        query = database.search_user(request.get_json())
        print(query)
        current_user = query["username"]
        render_template("settings.html")
    except:
        return render_template("login.html")


@app.route('/Settings/fetch/current_user', methods = ['GET'])
def fetch_current_user():
    print(current_user)
    try:
        print(current_user)
        return current_user
    except:
        return "none"    

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
   