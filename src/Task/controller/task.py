import json
from database import db
import datetime
from uuid import uuid4


class Task:
    def __init__(self, request, user_id):
        self.request = request
        self.input_data = json.loads(request.data)
        self.user_id = user_id

    def get(self, task_id):
        if task_id:
            tasks = db['Task'].find_one({'_id': task_id})
        else:
            tasks = list(db['Task'].find({'_user': self.user_id}))
        return {'message': '', 'data': tasks, 'status': True}, 200

    def post(self):
        task_object = {
            '_id': uuid4().hex,
            '_user': self.user_id,
            'task': {
                'name': 'New Task',
                'label': 'New Task',
                'type': 'simple_response',
                'security': 'public',
                'required': True,
                'description': '',
                'created_on': datetime.datetime.now(),
                'updated_on': datetime.datetime.now()
            },
            'utterances': [],
            'flow': [],
            'responses': []
        }
        task = db['Task'].insert_one(task_object)
        task = db['Task'].find_one({'_id': task.inserted_id})
        return {'message': 'successfully created', 'data': task, 'status': True}, 201

    def put(self, task_id):
        db['Task'].update_one(
            {'_id': task_id},
            {
                '$set': {
                    'flow': self.input_data['flow'],
                    'utterances': self.input_data['utterances'],
                    'task': self.input_data['task'],
                    'responses': self.input_data['responses']
                }
            }
        )
        return {'message': 'successfully updated', 'data': {}, 'status': True}, 200

    def delete(self, task_id):
        db['Task'].delete_one(
            {'_id': task_id}
        )
