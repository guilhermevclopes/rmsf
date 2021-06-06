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
import constructor

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

@app.route('/settings')
def settings():
    return render_template("settings.html")

# @app.route('/Auth/signup', methods = ['POST'])
# def auth_signup():
#     try:
#         resp = database.new_user(request.get)
#         print(resp)
#         if resp:
#             return redirect(url_for("login"))
#         else:
#             return redirect(url_for("home_page"))
#     except:
#             return redirect(url_for("home_page"))

# @app.route('/Auth/login', methods=['POST'])
# def auth_login():
#     try:
#         query = database.search_user(request.get_json())
#         print(query)
#         current_user = query["username"]
#         render_template("settings.html")
#     except:
#         return render_template("login.html")


# @app.route('/Settings/fetch/current_user', methods = ['GET'])
# def fetch_current_user():
#     print(current_user)
#     try:
#         print(current_user)
#         return current_user
#     except:
#         return "none"    

# @app.route('/Settings/update/<int:user>', methods = ['POST'])
# def update_settings(user):
#     try:
#         settings = database.update_settings(user, request.get_json())
#     except:
#         return 0
#     return 1


@app.route('/login/user', methods = ['POST'])
def user_login():
    username = request.form["username"]
    global current_user 
    current_user = username
    if(database.search_user(username)):
        return render_template("settings.html")
    
    return render_template("home.html")


@app.route('/signup/user', methods = ['POST'])
def user_signup():
    
    f = request.files.getlist("files")
    username = request.form["username"]
    os.mkdir(username)
    global current_user 
    current_user = username
    password = request.form["password"]

    if database.new_user(username, password):
        os.mkdir("dataset/"+username)
        for file in f:
            file.save("dataset/"+username+"/"+file.filename)

        os.system("python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog")


        return render_template("settings.html")
    return render_template("home.html")


@app.route('/user/settings', methods = ['POST'])
def update_settings():
    data = []
    data.append(request.form["news"])
    data.append(request.form["weather"])
    print(request.form)
    for x in range(3):
        i = str(x+1)
        m = "module"+i 
        if m in request.form:
            data.append("1")
        else:
            data.append("0")
    
    database.update_settings(current_user, data)
    constructor.constructor(current_user)

    return render_template("settings.html")

if __name__ == '__main__':
    app.run(port=5000,debug=True)
   