from flask_restful import Resource, reqparse
from models import UserModel
from flask import json
from run import mysql
import random
import string

register = reqparse.RequestParser()
auth = reqparse.RequestParser()
join = reqparse.RequestParser()
task = reqparse.RequestParser()
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

#Parser For Create Task
task.add_argument('id_user', help='this field cannot be blank', location='json', required= True)
task.add_argument('description', help='this field cannot be blank', location='json', required= True)
task.add_argument('name_location', help='this field cannot be blank', location='json', required= True)



def randomString():
    for x in range(100):
        return random.randint(1,1100000)
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


#==========This For Tables Task===================


class JoinTask(Resource):
    def post(self):
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


class ShowTask(Resource):
    def get(self, id_user=None):
        conn = mysql.connect()
        cursor = conn.cursor()
        result = cursor.execute("SELECT Task.id_task, Join_task.id_user, Task.description, Join_task.roles FROM Join_task JOIN User JOIN Task WHERE Join_task.id_task=Task.id_task AND Join_task.id_user=User.id_user AND Join_task.id_user= %s ",int(id_user))
        data = cursor.fetchall()
        results = []
        if(result):
            for item in data:
                dataResponse = {
                'id_task'     : item[0],
                'id_user'     : item[1],
                'descriptions'   : item[2],
                'roles'  : item[3],
            }
                results.append(dataResponse)
            return ({'success':'true',
                    'data':results})
        else:
            return json.dumps({'data':'null'})

class CreateTask(Resource):
    def post(self):
        data = task.parse_args()

        conn = mysql.connect()
        cursor = conn.cursor()
        id_task=randomString()
        id_user=data['id_user']
        result = cursor.execute(
        """INSERT INTO Task (
                id_task,    
                description,
                name_location
            ) 
            VALUES (%s,%s,%s)""",(id_task,data['description'],data['name_location']))
        conn.commit()
        conn.close()
        level='boss'
        if(result): 
            return JoinTask_Create(id_task,id_user,level, data['description'], data['name_location'])
        else:
            return {"success":"false"}

def JoinTask_Create(id_task, id_user, level, descriptions, name_location):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
        """INSERT INTO Join_task (
                id_task,
                id_user,
                roles
            ) 
            VALUES (%s,%s,%s)""",(id_task,id_user,level))
        conn.commit()
        conn.close()
        return {'success':'true',
                'data':{
                'id_task':id_task,
                'description':descriptions,
                'name_location':name_location
                }
                }


