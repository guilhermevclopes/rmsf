from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session
from sqlalchemy.orm import sessionmaker
from os import path

from sqlalchemy.sql.sqltypes import JSON


DATABASE_FILE = "magicmirror.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) 
Base = declarative_base()

class users(Base):
    __tablename__ = 'usersTable'
    username = Column(String, primary_key = True)
    password = Column(String)
    #settings = Column(JSON)
    def __repr__(self):
        return "<username=%s, password=%s>" % (self.username, self.password)
    def to_dictionary(self):
        return {"username": self.username, "password": self.password}


class settings(Base):
    __tablename__ = 'appSettingsTable'
    username = Column(String, primary_key=True)
    weather = Column(String) 
    module1 = Column(Integer, default = 1)
    module2 = Column(Integer, default = 0)
    module3 = Column(Integer, default = 0)
    #...
    def __repr__(self):
        return "<username id=%s, weather=%s>" % (self.username, self.weather)
    def to_dictionary(self):
        return {"username": self.username, "url": self.weather}

Base.metadata.create_all(engine) 
Session = sessionmaker(bind=engine)
session = scoped_session(Session)


def new_user(user):
    exists = session.query(users).filter(users.username==user["username"]).first()
    if exists == None:
        print(user["username"])
        print(user["password"])
        new = users(username = user["username"], password = user["password"])
        try:
            session.add(new)
            session.commit()
            session.close()
            return 1
        except:
            return None
    else:
        return 0


# def newUser(userData):
#     exists = session.query(users).filter(users.id==userData['username']).first()
#     if exists == None:
#         newEvent('NEW USER', userData['username'])
#         new = users(id = userData['username'], name = userData['name'], email = userData['email'], registeredVideos = 0, totalViews = 0, totalQuestions = 0, totalAnswers = 0)
#         try:
#             session.add(new)
#             session.commit()
#             session.close()
#             return 1
#         except:
#             return None
#     else:
#         return 0

def search_user(user):
    u = session.query(users).filter(users.username==user["username"]).first()
    session.close()
    return u

# def listVideos():
#     videosList = session.query(videos).all()
#     session.close()
#     return videosList

# def listVideosDICT():
#     ret_list = []
#     lv = listVideos()
#     for v in lv:
#         vd = v.to_dictionary()
#         del(vd["url"])
#         ret_list.append(vd)
#     return ret_list

# def newVideo(title, url, userID):
#     new = videos(title = title, url = url)
#     try:
#         session.add(new)
#         u = session.query(users).filter(users.id==userID).first()
#         u.registeredVideos+=1
#         session.commit()
#         n = new.id
#         session.close()
#         return n
#     except:
#         return None

# def getVideo(id):
#      v =  session.query(videos).filter(videos.id==id).first()
#      session.close()
#      return v

# def getVideoDICT(id):
#     return getVideo(id).to_dictionary()

# def newVideoView(id, userID):
#     b = session.query(videos).filter(videos.id==id).first()
#     u = session.query(users).filter(users.id==userID).first()
#     u.totalViews+=1
#     b.views+=1
#     n = b.views
#     session.commit()
#     session.close()
#     return n

# def newUser(userData):
#     exists = session.query(users).filter(users.id==userData['username']).first()
#     if exists == None:
#         newEvent('NEW USER', userData['username'])
#         new = users(id = userData['username'], name = userData['name'], email = userData['email'], registeredVideos = 0, totalViews = 0, totalQuestions = 0, totalAnswers = 0)
#         try:
#             session.add(new)
#             session.commit()
#             session.close()
#             return 1
#         except:
#             return None
#     else:
#         return 0
    
# def addQuestion(videoID, time, text, userID):
#     new = questions(videoID = videoID, time = time, text = text, userID = userID)
#     try:
#         session.add(new)
#         u = session.query(users).filter(users.id==userID).first()
#         u.totalQuestions+=1
#         session.commit()
#         n = new.id
#         session.close()
#         return n
#     except:
#         return None

# def addAnswer(questionID, text, userID):
#     new = answers(questionID = questionID, text = text, userID = userID)
#     try:
#         session.add(new)
#         u = session.query(users).filter(users.id==userID).first()
#         u.totalAnswers+=1
#         session.commit()
#         n = new.text
#         session.close()
#         return n
#     except:
#         return None

# def videoQuestions(videoID):
#     q = session.query(questions).filter(questions.videoID==videoID).all()
#     session.close()
#     return q

# def allVideoQuestions(videoID):
#     qList = videoQuestions(videoID)
#     ret_list = []

#     for q in qList:
#         aux = q.to_dictionary()
#         ret_list.append(aux)
#     return ret_list

# def allVideoAnswers(videoID):
#     questions = allVideoQuestions(videoID)
#     allA = []
#     for q in questions:
#         a = session.query(answers).filter(answers.questionID==q['id']).all()
#         for x in a:
#             aux = x.to_dictionary()
#             allA.append(aux)
#     return allA

# def getUsers():
#     u = session.query(users).all()
#     retL = []
#     for user in u:
#         aux = user.to_dictionary()
#         del(aux['email'])
#         retL.append(aux)
#     return retL

# def newEvent(event, user):
#     new = events(timestamp=datetime.now().strftime("%d/%b/%Y %H:%M:%S"), event=event, user=user)
#     try:
#         session.add(new)
#         session.commit()
#         n = new.event
#         session.close()
#         return n
#     except:
#         return None



# def newRequest(r, IP, e, user):
#     new = requests(timestamp=datetime.now().strftime("%d/%b/%Y %H:%M:%S"), request=r, IP=IP, epoint=e, user=user)
#     try:
#         session.add(new)
#         session.commit()
#         n = new.timestamp
#         session.close()
#         return n
#     except:
#         return None

# def getAllEvents():
#     e = session.query(events).all()
#     retL = []
#     for event in e:
#         aux = event.to_dictionary()
#         retL.append(aux)
#     return retL

# def getAllRequests():
#     r = session.query(requests).all()
#     retL = []
#     for request in r:
#         aux = request.to_dictionary()
#         retL.append(aux)
#     return retL

if __name__ == "__main__":
    pass