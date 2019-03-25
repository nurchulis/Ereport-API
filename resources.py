import os
from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel
from flask import json, request
from run import mysql
from run import app
from werkzeug import secure_filename
import random
import string
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

register = reqparse.RequestParser()
auth = reqparse.RequestParser()
join = reqparse.RequestParser()
task = reqparse.RequestParser()
edittask = reqparse.RequestParser()
file = reqparse.RequestParser()
task_data = reqparse.RequestParser()
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

#parser For Edit Task
edittask.add_argument('description', help='this field cannot be blank', location='json', required= True)
edittask.add_argument('name_location', help='this field cannot be blank', location='json', required= True)

file.add_argument('file[]', location=['headers', 'values'])

#data
task_data.add_argument('geolocation', help = 'This field cannot be blank',location='form', required = True)
task_data.add_argument('keterangan', help = 'This field cannot be blank',location='form', required = True)


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
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'success':'true',
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
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
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}


class GetUser(Resource):
    @jwt_required    
    def get(self, id_user=None):
        if not id_user:
            return 404
        # Do stuff
        return UserModel.find_by_user(id_user)

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}

class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()
    
    def delete(self):
        return UserModel.delete_all()





#==========This For Tables Task===================


class JoinTask(Resource):
    def post(self):
        data = join.parse_args()
        conn = mysql.connect()
        cursor = conn.cursor()

        result=cursor.execute("SELECT * from Join_task where id_task = %s AND id_user = %s", (data['id_task'], data['id_user']))
        
        if (result):
                return {'success':'false',
                        'message': 'Task already join'}
        else:  

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
    @jwt_required
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

class UpdateTask(Resource):
        def post(self, id_task=None):
            data = edittask.parse_args()            
            conn = mysql.connect()
            cursor = conn.cursor()
            result = cursor.execute("UPDATE Task SET description = %s, name_location = %s WHERE id_task = %s",
                            (data['description'],data['name_location'],int(id_task)))
            conn.commit()
            conn.close()
            if(result):
                return {'success':'true'}
            else:
                return {'success':'false'}

class Uploadgambar(Resource):
    def post(self):
        # Get the name of the uplo
        uploaded_files = request.files.getlist("file[]")
        filenames = []
        uniqe_name_data=randomString()
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                # Move the file form the temporal folder to the upload
                # folder we setup
                uniqe_name=randomFile()+filename

                
                insert(uniqe_name,uniqe_name_data)

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], uniqe_name))
                # Save the filename into a list, we'll use it later
                filenames.append(uniqe_name)
                # Redirect the user to the uploaded_file route, which
                # will basicaly show on the browser the uploaded file
        # Load an html page with a link to each uploaded file
        return {'success':'true'}


class UploadgambarWithData(Resource):
    def post(self, id_task=None):
        # Get the name of the uplo
        uploaded_files = request.files.getlist("file[]")
        data =task_data.parse_args()
        geolocation = data['geolocation']
        keterangan =data['keterangan']
        filenames = []
        uniqe_name_data=randomString()
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                uniqe_name=randomFile()+filename                
                
                insert(uniqe_name,uniqe_name_data)
                insert_data(int(id_task),geolocation,keterangan,uniqe_name_data)


                file.save(os.path.join(app.config['UPLOAD_FOLDER'], uniqe_name))
                filenames.append(uniqe_name)
        return {'success':'true'}

        

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def randomFile(stringLength=25):
    """Generate a random string of fixed length """
    letters= string.ascii_lowercase
    return ''.join(random.sample(letters,stringLength))


def insert(uniqe_name,uniqe_name_data):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
    """INSERT INTO Gambar (related_id,name_gambar) 
    VALUES (%s,%s)""",(uniqe_name_data,uniqe_name))
    conn.commit()
    conn.close()

def insert_data(id_task,geolocation,keterangan,uniqe_name_data):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
    """INSERT INTO Data (id_task,geolocation,keterangan,related_gambar) 
    VALUES (%s,%s,%s,%s)""",(id_task,geolocation,keterangan,uniqe_name_data))
    conn.commit()
    conn.close()

