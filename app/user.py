from flask import request
from flask_restful import fields, marshal_with, reqparse
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token)
from passlib.hash import pbkdf2_sha256 as sha256
import africastalking
from app.models import User

class UserApi(object):
    def __init__(self, email, phone_number, username, password):
        self.email = email
        self.phone_number = phone_number
        self.username = username
        self.password = password

    @staticmethod
    def generate_hash(password):

        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):

        return sha256.verify(password, hash)

user_fields = {
    'email': fields.String,
    'phone_number': fields.Integer,
    'username': fields.String,
    'password': fields.String
}

class UserRegister(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, help='please input email',
                                   location='json')
        self.reqparse.add_argument('phone_number', type=str, required=True, help='please input phone_No',
                                   location='json')
        self.reqparse.add_argument('username', type=str, required=True, help='please input username', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='please input password', location='json')

    def post(self, **kwargs):
        args = self.reqparse.parse_args()
        email = args['email']
        username = args['username']
        phone_number = args['phone_number']
        password = args['password']

        if not email.replace(" ", ""):
            return{"message": "email not valid"}
        elif not phone_number.replace(" ", ""):
            return {"message": "input phone_number"}
        elif not password.replace(" ", ""):
            return{"message": "input password"}
        elif not username.replace(" ", ""):
            return {"messsage": "input valid username"}

        user_data = User(**args)

        user = User.find_by_email(args['email'])

        if user:
            return {"message": "email already registered"}
        else:
            user_data.password = UserApi.generate_hash(user_data.password)
            user_data.save()
            return {
                "message": "User {0} was created".format(user_data.username)}

    @marshal_with(user_fields)
    def get(self):
        result = User.get_all()
        return result


class UserLogin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='please input username', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='please input password', location='json')

    def sms(self):
        args = self.reqparse.parse_args()
        user = User.find_by_username(args['username'])
        print(user)

        username = 'sandbox'
        apikey = '4ad25512763f7f60903a0a25e7c6f6af5c4a90688a1498b577836facc7c3080f'

        to = str(user.phone_number)
        phone_number = str("+") +str(254) + to[1:]
        print (phone_number)

        message = "to complete this process input this code: 1234567"


        #Initialize Sdk
        africastalking.initialize(username, apikey)

        #initialize a service
        sms = africastalking.SMS

        sms.send (message, [phone_number], callback=self.on_finish)

        # Or use it asynchoronously
    def on_finish(error, response):
        if error is not None:
            raise error
        print(response)

    def post(self):
        args = self.reqparse.parse_args()
        user = User.query.filter_by(username=args['username']).first()

        if not user:
            return {"message": "User{} doesn\'t exist".format(args['username'])}

        if UserApi.verify_hash(args.password, user.password):
            UserLogin.sms(self)
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            return {
                'message': 'Logged in as {}'.format(user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {
                'message': 'wrong credentials provided'
            }
