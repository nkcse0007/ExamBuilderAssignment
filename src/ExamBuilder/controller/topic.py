import json
from database import db
import datetime
from uuid import uuid4


class Topic:
    def __init__(self, request, exam_id, subcategory_id, subject_id, topic_id):
        self.request = request
        if request.method != 'GET':
            self.input_data = json.loads(request.data)
        self.exam_id = exam_id
        self.subcategory_id = subcategory_id
        self.subject_id = subject_id
        self.topic_id = topic_id

    def get(self):
        import pdb;pdb.set_trace()
        if self.topic_id:
            data = db['Topic'].find_one({'_id': self.topic_id})
        elif self.subject_id:
            data = db['Topic'].find_one({'_subject': self.subject_id})
        elif self.subcategory_id:
            data = db['Topic'].find_one({'_subcategory': self.subcategory_id})
        else:
            data = list(db['Topic'].find({'_exam': self.exam_id}))
        return {'message': '', 'data': data, 'status': True}, 200

    def post(self):
        if 'name' not in self.input_data or not self.input_data['name'] or type(self.input_data['name']) is not str:
            return {'message': 'Name is required', 'data': {}, 'status': False}, 400

        topic_object = {
            '_id': uuid4().hex,
            '_exam': self.exam_id,
            '_subcategory': self.subcategory_id if self.subcategory_id else '',
            '_subject': self.subject_id if self.subject_id else '',
            'type': 'TOPIC',
            'name': self.input_data['name'],
            'description': self.input_data['description'] if 'description' in self.input_data else '',
            'created_on': datetime.datetime.now().timestamp(),
            'updated_on': datetime.datetime.now().timestamp()
        }
        topic = db['Topic'].insert_one(topic_object)
        topic = db['Topic'].find_one({'_id': topic.inserted_id})
        return {'message': 'Topic successfully created', 'data': topic, 'status': True}, 201

    def put(self):
        if not self.topic_id or type(self.topic_id) is not str:
            return {'message': 'topic_id is required', 'data': {}, 'status': False}, 400
        self.input_data['updated_on'] = datetime.datetime.now().timestamp()
        db['Topic'].update_one(
            {'_id': self.topic_id},
            {
                '$set': self.input_data

            }
        )
        return {'message': 'Topic successfully updated', 'data': {}, 'status': True}, 200

    def delete(self):
        if not self.topic_id or type(self.topic_id) is not str:
            return {'message': 'topic_id is required', 'data': {}, 'status': False}, 400

        db['Topic'].delete_one(
            {'_id': self.topic_id}
        )
        return {'message': 'Topic deleted successfully', 'data': {}, 'status': True}, 200
