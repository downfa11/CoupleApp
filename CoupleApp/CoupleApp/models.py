from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class Bucketlist(db.Model):
    __tablename__ = 'Bucketlist'

    id = db.Column(db.Integer, primary_key = True)
    couple_id = db.Column(db.String(256), db.ForeignKey('mycouple.id'), nullable=False) # 이것을 기준으로 filterd_by
    title = db.Column(db.String(256))
    status = db.Column(db.Integer)
    due = db.Column(db.String(64))
    tstamp = db.Column(db.DateTime, server_default=db.func.now())  #현재시간 삽입기능
    

    @property
    def serialize(self) :
        return {
            'id':self.id,
            'mycouple':self.mycouple1.id,   
            'title': self.title,
        }


class Myuser(db.Model):
    __tablename__ = 'myuser'
    id = db.Column(db.Integer, primary_key = True)
    mycouple_id = db.Column(db.Integer, db.ForeignKey('mycouple.id'), nullable=True)
    userid = db.Column(db.String(128))
    hashcode = db.Column(db.String(128))
    @property
    def serialize(self) :
        return {
            'id':self.id,
            'mycouple':self.mycouple1.id,

        }
    
class Mycouple(db.Model):
    __tablename__ = 'mycouple'
    id = db.Column(db.Integer, primary_key = True)
    user1 = db.Column(db.String(128))
    user2 = db.Column(db.String(128))
    
    users = db.relationship('Myuser', backref = 'mycouple1', lazy=True)
    answ = db.relationship('Answer', backref = 'mycouple1', lazy=True)
    dday = db.Column(db.String(64))
    def serialize(self) :
        return {
            'id':self.id,
        }

class Question(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(128))
    answ = db.relationship('Answer', backref = 'quest', lazy=True)
    
class Answer(db.Model):
    __tablename__='answer'
    id = db.Column(db.Integer,primary_key=True)
    question_id= db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    couple_id= db.Column(db.String(128), db.ForeignKey('mycouple.id'), nullable=False)
    answer1= db.Column(db.String(128))
    answer1_id= db.Column(db.String(128))
    answer2= db.Column(db.String(128))
    answer2_id= db.Column(db.String(128))
    tstamp = db.Column(db.DateTime, server_default=db.func.now())
    
    @property
    def serialize(self) :
        return {
            'id':self.id,
            'mycouple':self.mycouple1.id,
            'question':self.quest.id,
        }