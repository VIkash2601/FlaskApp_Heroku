from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This item cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store_id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item does not exists!'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {'message':
                "An item with name '{}' already exists.".format(name)}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500
        return item.json(), 201


    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted.'}

    @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)
        if item:
            try:
                item.price = request_data['price']
            except:
                return {'message': 'An error occurred inserting the item.'}, 500
        else:
            try:
                item = ItemModel(name, **request_data)
            except:
                return {'message': 'An error occurred updating the item.'}, 500

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
