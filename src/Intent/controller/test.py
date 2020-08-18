import os
from flask import Blueprint, request, jsonify
from deeppavlov import build_model
from src.CommonHelpers.com import *
from src.CommonHelpers.config import *
from database import db

url = os.environ.get('URL')
intent_app = Blueprint('intent_route', __name__, template_folder='templates')
ROOT_PATH = os.path.dirname(os.path.abspath('app.py'))
MEDIA_PATH = f"{ROOT_PATH}/{os.environ.get('MEDIA_FOLDER')}"


def test_intent(user_id):
    data = json.loads(request.data)
    if 'question' not in data or data['question'] == '':
        return {'message': 'question is required', 'data': {}, 'status': True}, 400
    else:
        config_file = intent_config(f"{MEDIA_PATH}/task_files/user_{user_id}")
        try:
            import pdb;pdb.set_trace()
            model = build_model(config_file, download=True)
            response_id = model([data['question']])[0][0]
            if not response_id:
                return {'message': '',
                        'data': {'answer': 'sorry not able to understand, please try  rephrasing'}, 'status': True}, 200
            else:
                response = db['Task'].find_one(
                    {'_id': response_id},
                    {'responses': 1, 'label': 1}
                )
                return {'message': '', 'data': {'answer': response}, 'response_id': response_id, 'status': True}, 200
        except Exception as e:
            print(e)
            return {'message': 'error! files are not ready, please train it first ' + str(e), 'data': {},
                    'status': False}, 400