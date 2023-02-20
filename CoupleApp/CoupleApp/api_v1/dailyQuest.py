from flask import jsonify, request,Blueprint,session, redirect
import requests
from . import api
from models import Question,Answer, db, Mycouple


@api.route('/quests', methods=['GET','POST','DELETE','PUT'])
def quests():
    coupleid = session.get('coupleid')
    questid = session.get('questid')
    userid = session.get('userid')
    data = request.get_json()
    
    if request.method == 'POST':   #POST - 할일을 생성할때의 메서드
        answer = Answer.query.filter_by(couple_id=coupleid).first()
        if answer==None:  ## Add
            answer=Answer()
            answer.couple_id=coupleid
            answer.question_id=questid
            if answer.answer1==None:
                answer.answer1 = data.get('answer')
                answer.answer1_id=userid
                    
            elif answer.answer2==None:
                answer.answer2 = data.get('answer')
                answer.answer2_id=userid

            db.session.add(answer)
            
        else:   ## Modify
            answer = answer.query.filter_by(question_id=questid).first()
            answer.couple_id=coupleid
            if answer.answer1_id==userid:
                answer.answer1 = data.get('answer')
            else:
                answer.answer2 = data.get('answer')
            db.session.commit()
            
        
        
	#elif request.method == 'GET':
    #    bucketlist = bucketlist.query.filter_by(myuser_id=userid)
    #    return jsonify([t.serialize for t in quests])

    elif request.method == 'PUT':
        answer = Answer.query.filter_by(couple_id=coupleid).first()
        answer = answer.query.filter_by(question_id=questid).first()
        if answer.answer1_id==userid:
            answer.answer1 = None
        elif answer.answer2_id==userid:
            answer.answer2 = None
        
        db.session.commit()
        #db.session.delete(answer) #초기화할떄 사용..

        return jsonify(), 203



    db.session.commit()
    return jsonify(data)

