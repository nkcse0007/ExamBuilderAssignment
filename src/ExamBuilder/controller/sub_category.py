import json
from database import db
import datetime
from uuid import uuid4


class SubCategory:
    def __init__(self, request, exam_id, subcategory_id):
        self.request = request
        if request.method != 'GET':
            self.input_data = json.loads(request.data)
        self.exam_id = exam_id
        self.subcategory_id = subcategory_id

    def get(self):
        if self.subcategory_id:
            data = db['SubCategory'].find_one({'_id': self.subcategory_id})
        else:
            data = list(db['SubCategory'].find({'_exam': self.exam_id}))
        return {'message': '', 'data': data, 'status': True}, 200

    def post(self):
        if 'name' not in self.input_data or not self.input_data['name'] or type(self.input_data['name']) is not str:
            return {'message': 'name is required', 'data': {}, 'status': False}, 400

        subcategory_object = {
            '_id': uuid4().hex,
            '_exam': self.exam_id,
            'type': 'SUBCATEGORY',
            'name': self.input_data['name'],
            'description': self.input_data['description'] if 'description' in self.input_data else '',
            'created_on': datetime.datetime.now().timestamp(),
            'updated_on': datetime.datetime.now().timestamp()
        }
        subcategory = db['SubCategory'].insert_one(subcategory_object)
        subcategory = db['SubCategory'].find_one({'_id': subcategory.inserted_id})
        return {'message': 'Sub Category successfully created', 'data': subcategory, 'status': True}, 201

    def put(self):
        if not self.subcategory_id or type(self.subcategory_id) is not str:
            return {'message': 'subcategory_id is required', 'data': {}, 'status': False}, 400
        self.input_data['updated_on'] = datetime.datetime.now().timestamp()
        db['SubCategory'].update_one(
            {'_id': self.subcategory_id},
            {
                '$set': self.input_data

            }
        )
        return {'message': 'Sub Category successfully updated', 'data': {}, 'status': True}, 200

    def delete(self):
        if not self.subcategory_id or type(self.subcategory_id) is not str:
            return {'message': 'subcategory_id is required', 'data': {}, 'status': False}, 400

        db['SubCategory'].delete_one(
            {'_id': self.subcategory_id}
        )
        return {'message': 'Sub Category deleted successfully', 'data': {}, 'status': True}, 200
