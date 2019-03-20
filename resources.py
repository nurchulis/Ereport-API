from flask_restful import Resource, reqparse
from models import UserModel
from flask import json

parser = reqparse.RequestParser()
parsing = reqparse.RequestParser()
#parser.add_argument('username', help = 'This field cannot be blank',location='form', required = True)
parser.add_argument('username', help = 'This field cannot be blank',location='form', required = True)
parser.add_argument('password', help = 'This field cannot be blank',location='form', required = True)
parsing.add_argument('email', help= 'This field cannot be blank', required = True)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'. format(data['username'])}
        
        if UserModel.find_by_email(data['email']):
            return {'message': 'Email {} already exists'. format(data['email'])}

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password']),
            email    = data['email']
        )

        try:
            new_user.save_to_db()
            return {
                'status':'true',
                'message': 'User {} was created'.format( data['username'])
            }
        except:
            return {'status': 'false'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            return {
            'status':'true',
            'message': 'Logged in as {}'.format(current_user.username)}
        else:
            return {'message': 'Wrong credentials'}


class GetUser(Resource):
    def get(self, id_user=None, username=None):
        if not id_user:
            return 404
        # Do stuff
        return UserModel.find_by_user(id_user, username)



class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}


class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}


class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()
    
    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }