from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask import json
from flaskext.mysql import MySQL
from flask_jwt_extended import JWTManager

app = Flask(__name__)

api = Api(app)
mysql = MySQL()

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

#--------_For Sqlalchemy Tools------------#
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ereport'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asnaksw12i10201sask'

#---------_For Mysql----------------------#
# mysql_configuratoin
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = 'root'
app.config['MYSQL_DATABASE_DB']         = 'ereport'
mysql.init_app(app)

db = SQLAlchemy(app) 

import views, models, resources
path_api ='/api/v1'

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
@app.before_first_request
def create_tables():
    db.create_all()

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401


#authentification
api.add_resource(resources.UserRegistration, path_api+'/registration')
api.add_resource(resources.UserLogin, path_api+'/login')
api.add_resource(resources.UserLogoutAccess, path_api+'/logout/access')



#User
api.add_resource(resources.GetUser,path_api+'/User/<int:id_user>')



#Task
api.add_resource(resources.JoinTask, path_api+'/JoinTask')
api.add_resource(resources.ShowTask, path_api+'/ShowTask/<int:id_user>')
api.add_resource(resources.CreateTask, path_api+'/CreateTask')
api.add_resource(resources.UpdateTask, path_api+'/UpdateTask/<int:id_task>')

#Data
api.add_resource(resources.Uploadgambar, path_api+'/SendImageMulti')
api.add_resource(resources.UploadgambarWithData, path_api+'/SendDataTask')


api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, path_api+'/token/refresh')
api.add_resource(resources.AllUsers, '/users')

if __name__ == '__main__':
    app.run()
