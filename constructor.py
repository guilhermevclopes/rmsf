import os
import json
import database

def constructor(username):
    settings = database.get_settings(username)
    print(settings)

    news_dict = {"RTP": "https://www.rtp.pt/noticias/rss/pais", "JN": "http://feeds.jn.pt/JN-Ultimas", "NYT": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"}
    weather_dict = {"Lisbon,Portugal": "2267057", "Porto,Portugal":"2735943", "Algarve,Portugal":"2268339"}

    for i in settings:
        if settings[i] == 1:
            settings[i] = False
        elif settings[i] == 0:
            settings[i] = True

    print (settings)
    data = json.load(open("config.json",'r'))

    exc = [1,2,3]
    for i in range(len(data["modules"])):
        if i not in exc:
            data["modules"][i]["classes"] = username        

    data["modules"][4]["disabled"] = settings["clock"] #clock
    data["modules"][5]["disabled"] = settings["calendar"] #calendar
    data["modules"][6]["disabled"] = settings["compliments"] #compliments
    
    if settings["weather"] == 'none':
        data["modules"][7]["disabled"] = True #weather    
    else:
        data["modules"][7]["disabled"] = False #weather    
        data["modules"][7]["config"]["location"] = "" #weather
        data["modules"][7]["config"]["locationID"] = weather_dict[settings["weather"]] #weather

    if settings["news"] == 'none':
        data["modules"][8]["disabled"] = True #newsfeed
    else:
        data["modules"][8]["disabled"] = False #newsfeed
        data["modules"][8]["config"]["feeds"][0]["title"] = settings["news"] #newsfeed
        data["modules"][8]["config"]["feeds"][0]["url"] = news_dict[settings["news"]] #newsfeed
    
    json.dump(data,open(username+'/config.json', 'w'))

if __name__ == '__main__':
    constructor("gui")