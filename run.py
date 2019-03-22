from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask import json
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)
mysql = MySQL()

#--------_For Sqlalchemy Tools------------#
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ereport'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asnaksw12i10201sask'

#---------_For Mysql----------------------#
# mysql configuratoin
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = 'root'
app.config['MYSQL_DATABASE_DB']         = 'ereport'
mysql.init_app(app)

db = SQLAlchemy(app) 

import views, models, resources
path_api ='/api/v1'


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


api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')

if __name__ == '__main__':
    app.run()
