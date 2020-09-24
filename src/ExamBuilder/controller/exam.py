import json
from database import db
import datetime
from uuid import uuid4


class Exam:
    def __init__(self, request, exam_id):
        self.request = request
        if request.method != 'GET':
            self.input_data = json.loads(request.data)
        self.exam_id = exam_id

    def get(self):
        if self.exam_id:
            data = db['Exam'].aggregate([
                {'$match': {'_id': self.exam_id}},
                {
                    '$lookup':
                        {
                            'from': 'SubCategory',
                            'let': {'examId1': '$_id'},
                            'pipeline': [
                                {'$match':
                                    {'$expr':
                                        {'$and':
                                            [
                                                {'$eq': ["$_exam", "$$examId1"]}
                                            ]
                                        }
                                    }
                                }, {
                                    '$lookup':
                                        {
                                            'from': 'Subject',
                                            'let': {'subcatId': '$_id', 'examId': '_exam'},
                                            'pipeline': [
                                                {'$match':
                                                    {'$expr':
                                                        {'$or':
                                                            [
                                                                {'$eq': ["$subcategory", "$$subcatId"]},
                                                                {'$eq': ["$_exam", "$$examId1"]}
                                                            ]
                                                        }
                                                    }
                                                }, {
                                                    '$lookup':
                                                        {
                                                            'from': 'Topic',
                                                            'let': {'subjectId': '$_id', 'examId': '_exam'},
                                                            'pipeline': [
                                                                {'$match':
                                                                    {'$expr':
                                                                        {'$or':
                                                                            [
                                                                                {'$eq': ["$_subject", "$$subjectId"]},
                                                                                {'$eq': ["$_exam", "$$examId1"]}
                                                                            ]
                                                                        }
                                                                    }
                                                                },

                                                            ],
                                                            'as': 'topic'
                                                        }
                                                }

                                            ],
                                            'as': 'subjects'
                                        }
                                }

                            ],
                            'as': 'data'
                        }
                }
            ])
        else:
            data = list(db['Exam'].find({}))
        return {'message': '', 'data': data, 'status': True}, 200

    def post(self):
        if 'name' not in self.input_data or not self.input_data['name'] or type(self.input_data['name']) is not str:
            return {'message': 'Name is required', 'data': {}, 'status': False}, 400

        exam_object = {
            '_id': uuid4().hex,
            'name': self.input_data['name'],
            'type': 'EXAM',
            'description': self.input_data['description'] if 'description' in self.input_data else '',
            'created_on': datetime.datetime.now().timestamp(),
            'updated_on': datetime.datetime.now().timestamp()
        }
        exam = db['Exam'].insert_one(exam_object)
        exam = db['Exam'].find_one({'_id': exam.inserted_id})
        return {'message': 'Exam successfully created', 'data': exam, 'status': True}, 201

    def put(self):
        if not self.exam_id or type(self.exam_id) is not str:
            return {'message': 'Name is required', 'data': {}, 'status': False}, 400
        self.input_data['updated_on'] = datetime.datetime.now().timestamp()
        import pdb;
        pdb.set_trace()
        db['Exam'].update_one(
            {'_id': self.exam_id},
            {
                '$set': self.input_data

            }
        )
        return {'message': 'Exam successfully updated', 'data': {}, 'status': True}, 200

    def delete(self):
        db['Exam'].delete_one(
            {'_id': self.exam_id}
        )
        return {'message': 'Exam deleted successfully', 'data': {}, 'status': True}, 200
