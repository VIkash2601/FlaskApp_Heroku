import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# for Heroku with local db as the environment database can't be there sometimes
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
                                            'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Allows Flask-JWT to return its specific errors and their status codes.
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'shiva'

api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList,'/stores')

if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run(port=5000, debug=True)
