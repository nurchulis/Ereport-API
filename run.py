from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask import json

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ereport'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asnaksw12i10201sask'

db = SQLAlchemy(app) 

import views, models, resources
path_api ='/api/v1'


#authentification
api.add_resource(resources.UserRegistration, path_api+'/registration')
api.add_resource(resources.UserLogin, path_api+'/login')
api.add_resource(resources.UserLogoutAccess, path_api+'/logout/access')



#User
api.add_resource(resources.GetUser,path_api+'/User/<int:id_user>/<username>')



#Task

api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')