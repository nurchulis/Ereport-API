from flask_restful import Resource, reqparse
from models import UserModel
from flask import json
from run import mysql

register = reqparse.RequestParser()
auth = reqparse.RequestParser()
join = reqparse.RequestParser()
#parser.add_argument('username', help = 'This field cannot be blank',location='form', required = True)
register.add_argument('username', help = 'This field cannot be blank', required = True)
register.add_argument('password', help = 'This field cannot be blank', required = True)
register.add_argument('email', help= 'This field cannot be blank', required = True)

auth.add_argument('username', help = 'This field cannot be blank or use json body Parameter', location='json', required = True)
auth.add_argument('password', help = 'This field cannot be blank or use json body Parameter', location='json', required = True)

#Parser For Join Task
join.add_argument('id_task', help='this field cannot be blank', location='json', required= True)
join.add_argument('id_user', help='this field cannot be blank', location='json', required= True)
join.add_argument('roles', help='this field cannot be blank', location='json', required= True)

class UserRegistration(Resource):
    def post(self):
        data = register.parse_args()

        if UserModel.find_by_username(data['username']):
            return {
            'success':'false',
            'message': 'User {} already exists'. format(data['username'])}
        
        if UserModel.find_by_email(data['email']):
            return {
            'success':'false',
            'message': 'Email {} already exists'. format(data['email'])}

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password']),
            email    = data['email']
        )

        try:
            new_user.save_to_db()
            return {
                'success':'true',
                'message': 'User {} was created'.format( data['username'])
            }
        except:
            return {'success': 'false'}, 500


class UserLogin(Resource):
    def post(self):
        data = auth.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {
            'success':'false',
            'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            return {
            'status':'true',
            'message': 'Logged in as {}'.format(current_user.username)}
        else:
            return {'success': 'false',
                    'message': 'Parameter invalid use Json please'}, 500


class GetUser(Resource):
    def get(self, id_user=None):
        if not id_user:
            return 404
        # Do stuff
        return UserModel.find_by_user(id_user)

class JoinTask(Resource):
    def get(self):
        data = join.parse_args()
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
        """INSERT INTO Join_task (
                id_task,
                id_user,
                roles
            ) 
            VALUES (%s,%s,%s)""",(data['id_task'],data['id_user'],data['roles']))
        conn.commit()
        conn.close()
        return {'success':'true'}
        

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