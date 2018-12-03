import json

from flask_restful import Resource, reqparse, fields, marshal, abort
from app.models import Bucketlist

Bucket_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
 }


class BucketListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No name provided', location='json')
        super(BucketListAPI, self).__init__()

    def get(self):

        results = Bucketlist.get_all()
        return {'results': [marshal(results, Bucket_fields) for result in results]}

    def post(self, **kwargs):
        args = self.reqparse.parse_args()
        name = args['name']
        Bucket_list = {'name': name}
        Bucket_list = Bucketlist( **args)
        if name:
            Bucket_list.save()
            return marshal(Bucket_list, Bucket_fields),201


class BucketAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No name provided', location='json')
        super(BucketAPI, self).__init__()


    def get(self, id):

        bucketlists =  Bucketlist.query.filter_by(id=id).first()

        if bucketlists:
            return {'result': marshal(bucketlists, Bucket_fields)},200
        else:
            abort(404)

    def put(self, id):
        args = self.reqparse.parse_args()
        name = args['name']
        if not name.replace(" ", ""):
            return {"message": "can't post an empty name"}, 400
        bucketlists = Bucketlist.query.filter_by(id=id).first()
        if bucketlists:
            bucketlists.name = name
            bucketlists.save()
            return {'result': marshal(bucketlists, Bucket_fields)},200
        else:
            abort(404)

    def delete(self, id):
        bucketlists = Bucketlist.query.filter_by(id=id).first()
        if bucketlists:
            bucketlists.delete()
            return {"message": "Bucketlist {} deleted successfully".format(bucketlists.id)},200
        else:
            abort(404)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}