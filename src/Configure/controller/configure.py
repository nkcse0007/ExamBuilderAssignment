import json
from database import db
import datetime
from uuid import uuid4


class Configure:
    def __init__(self, request, user_id):
        self.request = request
        self.input_data = json.loads(request.data)
        self.user_id = user_id

    def get(self):
        configure = db['User'].find_one({'_id': self.user_id}, {'configure': 1})
        return {'data': configure, 'status': True}, 200

    def put(self, task_id):
        db['Configure'].insert_one(
            {'_user': task_id},
            self.input_data
        )
