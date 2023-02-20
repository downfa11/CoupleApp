from datetime import datetime,timedelta
from flask import jsonify, request,Blueprint,session, redirect
import requests
from . import api
from models import db, Mycouple


@api.route('/ddays', methods=['GET','PUT'])
def dday():
    coupleid = session.get('coupleid') ### userid를 담은 couple의 id index를 session에 담아야함.
    data = request.get_json()
    
    if request.method == 'PUT':   #POST - 할일을 생성할때의 메서드
        temp=data.get('due')
        mycouple = Mycouple()
        couple = mycouple.query.filter_by(id=coupleid).first()
        couple.dday = temp
        db.session.commit()
        
    #elif request.method == 'GET':
    #    mycouple = mycouple.query.filter_by(index=index)
    #    return jsonify([t.serialize for t in ddays])


    db.session.commit()
    return jsonify(data)





'''
sqlalchemy.exc.InvalidRequestError: Entity namespace for "mycouple" has no property "index"


'''