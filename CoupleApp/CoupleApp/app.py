import os
from forms import CoupleForm
from flask import Flask,request,render_template , redirect, session,request,url_for
from api_v1 import api as api_v1
from models import db, Myuser, Bucketlist,Mycouple,Question,Answer
from datetime import datetime,timedelta
from oauth2client.contrib.flask_util import UserOAuth2

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1')
app.config['SECRET_KEY'] = '키키키키'

app.config['GOOGLE_OAUTH2_CLIENT_ID'] = '1093518041636-vfg70vjvflookd95g6mu35jb9vmcr0oo.apps.googleusercontent.com'
app.config['GOOGLE_OAUTH2_CLIENT_SECRET'] = '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'
oauth2 = UserOAuth2(app)



@app.route('/',methods=['GET'])
def home():
    bucketlists = []
    ddays=[]
    d_day=0
    quests=[]
    questlist=[]
    answerlist=[]
    answer=[]
    myanswer=None
    uranswer=None
    myuser = Myuser.query.filter_by(userid=oauth2.user_id).first()
    if myuser == None:
    	return redirect('/login')
    if oauth2.has_credentials(): 
        userid = oauth2.user_id
        session['userid']=userid
        if myuser.hashcode==None:
                return redirect('/access')

        couple=Mycouple.query.filter_by(user1=oauth2.user_id).first()
        if couple == None:
            couple=Mycouple.query.filter_by(user2=oauth2.user_id).first()
            
        bucketlists = Bucketlist.query.filter_by(couple_id=couple.id)
        session['coupleid']=couple.id
        session['questid']=0#quests[0].question_id
        quests = Question.query.filter_by(question_id=questid).first()
        answer=Answer.query.filter_by(couple_id=couple.id).first()
        if answer:
            answer__=answer.query.filter_by(question_id=session['questid']).first()
            if answer__:
                if answer__.answer1_id==userid:
                    myanswer=answer__.answer1
                    uranswer=answer__.answer2
                    
                else:
                    answer__.answer2_id=userid
                    myanswer=answer__.answer2
                    uranswer=answer__.answer1

        now = datetime.utcnow()
        d_day=0
        if couple.dday:
            ddays=datetime.strptime(couple.dday,'%m/%d/%Y')
            days=str(now-ddays).split('days') #사귄지 하루된 상태일때는 9:11:48.160964 시간이 뜬다.
            d_day=days[0]

        questlist=Question.query.all() # 근데 사실 이거도 이미 등록된 답변들의 리스트를 가져와야해서 따로 손봐야함.
        answerlist=Answer.query.filter_by(couple_id=couple.id)
    return render_template('home.html',userid=session['userid'],bucketlists=bucketlists
                                       ,ddays=ddays,d_day=d_day,quests=quests,answer=answer
                                          ,questlist=questlist
                           ,answerlist=answerlist,myanswer=myanswer,uranswer=uranswer)

@app.route('/error1')
def error():
    return render_template('error1.html')

        
        
        
@app.route('/login',methods=['GET','POST'])
@oauth2.required
def login():
    if oauth2.has_credentials():
        myuser = Myuser.query.filter_by(userid=oauth2.user_id).first()
        if myuser is None:
            myuser = Myuser()
            myuser.userid=oauth2.user_id
            db.session.add(myuser)
            db.session.commit()
        print( "Email : {}  UserID : ({})".format(oauth2.email, myuser.userid))
        session['userid'] = oauth2.user_id
        return redirect('/')
    else:
        return render_template('error1.html')

@app.route('/logout',methods=['GET'])  
def logout():

    return redirect('/')

@app.route('/access',methods=['GET','POST'])
def access():
    form = CoupleForm()
    myuser=Myuser()
    mycouple = Myuser.query.filter_by(hashcode=oauth2.user_id).first() 
    if not mycouple:
        print('아직 나를 가등록한 계정이 없습니다.')
        
    if form.validate_on_submit():
        
        temp = form.data.get('hashcode')
        wantcouple = Myuser.query.filter_by(userid=temp).first()
        if wantcouple is None: #원래는 이미 커플인 인원인지도 확인해야한다.
            print(temp,'는 커플앱에 가입하지 않은 유저입니다.')
        elif wantcouple.hashcode==None:
            user=Myuser.query.filter_by(userid=oauth2.user_id).first()
            user.hashcode=temp ## 커플 가등록 상태.
            db.session.add(user)
            db.session.commit()
            return redirect('/wait')
        elif wantcouple.hashcode==oauth2.user_id:
            user=Myuser.query.filter_by(userid=oauth2.user_id).first()
            user.hashcode=temp
            userid=oauth2.user_id
            return redirect('/')
        else:
            print('연동 실패')
        
    return render_template('access.html',form=form)

@app.route('/wait',methods=['GET','POST'])
def wait():
    myuser=Myuser.query.filter_by(userid=oauth2.user_id).first()
    mycouple = Myuser.query.filter_by(userid=myuser.hashcode).first()
    print(myuser," :",oauth2.user_id," myuser.hashcode :",myuser.hashcode, "mycouple.hashcode :",mycouple.hashcode)
    if myuser.hashcode and mycouple.hashcode == oauth2.user_id: #본인이 가등록한 상태고, 나를 가등록한 커플계정 역시 존재할때.
        couple=Mycouple()
        couple.user1=myuser.userid
        couple.user2=myuser.hashcode
        db.session.add(couple)
        db.session.commit()
        print("연동 성공!",couple.user1,couple.user2)
        return redirect('/')

        
    return render_template('access_wait.html')

@app.route('/manages',methods=['GET','POST'])
def manage():
    questionlists=[]
    questionlists = Question.query.filter_by()
    return render_template('manage.html',questionlists=questionlists)

basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir,'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password'
db.init_app(app)
db.app = app
db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True    )