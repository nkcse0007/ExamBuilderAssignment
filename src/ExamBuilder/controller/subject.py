import json
from database import db
import datetime
from uuid import uuid4


class Subject:
    def __init__(self, request, exam_id, subcategory_id, subject_id):
        self.request = request
        if request.method != 'GET':
            self.input_data = json.loads(request.data)
        self.exam_id = exam_id
        self.subcategory_id = subcategory_id
        self.subject_id = subject_id

    def get(self):

        if self.subject_id:
            data = db['Subject'].find_one({'_id': self.subject_id})
        elif self.subcategory_id:
            data = db['Subject'].find_one({'_subcategory': self.subcategory_id})
        else:
            data = list(db['Subject'].find({'_exam': self.exam_id}))
        return {'message': '', 'data': data, 'status': True}, 200

    def post(self):
        if 'name' not in self.input_data or not self.input_data['name'] or type(self.input_data['name']) is not str:
            return {'message': 'Name is required', 'data': {}, 'status': False}, 400

        subject_object = {
            '_id': uuid4().hex,
            '_exam': self.exam_id,
            'subcategory': self.subcategory_id if self.subcategory_id else '',
            'type': 'SUBJECT',
            'name': self.input_data['name'],
            'description': self.input_data['description'] if 'description' in self.input_data else '',
            'created_on': datetime.datetime.now().timestamp(),
            'updated_on': datetime.datetime.now().timestamp()
        }
        subject = db['Subject'].insert_one(subject_object)
        subject = db['Subject'].find_one({'_id': subject.inserted_id})
        return {'message': 'Subject successfully created', 'data': subject, 'status': True}, 201

    def put(self):
        if not self.subject_id or type(self.subject_id) is not str:
            return {'message': 'subject_id is required', 'data': {}, 'status': False}, 400
        self.input_data['updated_on'] = datetime.datetime.now().timestamp()
        db['Subject'].update_one(
            {'_id': self.subject_id},
            {
                '$set': self.input_data

            }
        )
        return {'message': 'Subject successfully updated', 'data': {}, 'status': True}, 200

    def delete(self):
        if not self.subject_id or type(self.subject_id) is not str:
            return {'message': 'subject_id is required', 'data': {}, 'status': False}, 400

        db['Subject'].delete_one(
            {'_id': self.subject_id}
        )
        return {'message': 'Subject deleted successfully', 'data': {}, 'status': True}, 200
