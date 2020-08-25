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
            model = build_model(config_file, download=True)
            response = model([data['question']])
            response_id = response[0][0]
            score = response[1][0][0]
            import pdb;pdb.set_trace()
            threshold = 0.50
            if not response_id:
                return {'message': 'training done',
                        'data': {'answer': 'sorry not able to understand, please try  rephrasing'}, 'status': True}, 200
            elif score < threshold:
                return {'message': 'training done',
                        'data': {'answer': 'Sorry not able to understand, please try  rephrasing'},
                        'status': True}, 200
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


def find_answer(user, req):
    try:
        login_data = db['VoiceLogin'].find_one({'platform_id':
                                                    req['originalDetectIntentRequest']['payload']['conversation'][
                                                        'conversationId']})
        user = db['User'].find_one({'_id': login_data['_user']})
        config_file = intent_config(f"{MEDIA_PATH}/task_files/user_{user['_id']}")
        if login_data['is_login'] is False:
            answer = {
                'label': 'Please ask my your query!!!',
                'type': 'simple_response'
            }
            db['VoiceLogin'].update_one(
                {'platform_id':
                     req['originalDetectIntentRequest']['payload']['conversation'][
                         'conversationId']},
                {'$set': {
                    'is_login': True
                }}
            )
        else:
            model = build_model(config_file, download=True)
            response_id = model([req['queryResult']['queryText']])[0][0]
            if not response_id:
                answer = {
                    'label': 'sorry not able to understand, please try  rephrasing',
                    'type': 'simple_response'
                }
            else:
                response = db['Task'].find_one(
                    {'_id': response_id},
                    {'responses': 1, 'label': 1}
                )
                answer = response['responses'][0]
    except Exception as e:
        print(e)
        return {'message': 'error! files are not ready, please train it first ' + str(e), 'data': {},
                'status': False}
    return answer
