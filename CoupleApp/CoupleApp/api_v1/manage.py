from flask import jsonify, request,Blueprint,session, redirect
import requests
from . import api
from models import Question, db, Mycouple


@api.route('/manages', methods=['GET','POST','DELETE','PUT'])
def manages():
    data = request.get_json()
    if request.method == 'POST':   #POST - 할일을 생성할때의 메서드
        question=Question()
        question.title = data.get('title')
        db.session.add(question)
        
	#elif request.method == 'GET':
    #    bucketlist = bucketlist.query.filter_by(myuser_id=userid)
    #    return jsonify([t.serialize for t in bucketlists])

    elif request.method == 'DELETE':
        question_id = data.get('question_id')
        question = Question.query.filter_by(id=question_id).first()
        db.session.delete(question)
        
        return jsonify(), 203


    elif request.method == 'PUT':
        data = request.get_json()
        question_id = data.get('question_id')
        question = Question.query.filter_by(id=question_id).first()
        db.session.commit()

        return jsonify()



    db.session.commit()
    return jsonify(data)

