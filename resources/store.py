from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_item_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store does not exists!'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_item_by_name(name):
            return {'message':
                "An store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred inserting the store.'}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_item_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted.'}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        # return {'stores': [x.json() for x in StoreModel.query.all()]}
        return {'stores': [x.json() for x in StoreModel.find_all()]}
