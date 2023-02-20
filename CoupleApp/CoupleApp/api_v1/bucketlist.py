from flask import jsonify, request,Blueprint,session, redirect
import requests
from . import api
from models import Bucketlist, db, Mycouple


@api.route('/bucketlists', methods=['GET','POST','DELETE','PUT'])
def bucketlists():
    coupleid = session.get('coupleid')

    data = request.get_json()
    
    if request.method == 'POST':   #POST - 할일을 생성할때의 메서드
        bucketlist=Bucketlist()
        bucketlist.title = data.get('title')
        mycouple = Mycouple.query.filter_by(id=coupleid).first()
        bucketlist.couple_id = mycouple.id
        bucketlist.due = data.get('due')
        bucketlist.status = 0
        db.session.add(bucketlist)
        
        
	#elif request.method == 'GET':
    #    bucketlist = bucketlist.query.filter_by(myuser_id=userid)
    #    return jsonify([t.serialize for t in bucketlists])

    elif request.method == 'DELETE':
        bucket_id = data.get('bucket_id')
        bucketlist = Bucketlist.query.filter_by(id=bucket_id).first()
        db.session.delete(bucketlist)
        
        return jsonify(), 203


    elif request.method == 'PUT':
        data = request.get_json()
        bucket_id = data.get('bucket_id')
        bucketlist = Bucketlist.query.filter_by(id=bucket_id).first()
        bucketlist.status = 1
        db.session.commit()

        return jsonify()



    db.session.commit()
    return jsonify(data)

