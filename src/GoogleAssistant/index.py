import os
import requests
from flask import Flask, Blueprint, request, jsonify, abort, make_response
from src.Faqs.file_upload import Files
from src.Faqs.train import train_faq
from src.Faqs.test import TestFaq
from src.Authentication.Controller.user import Register, Login
from flask_pymongo import PyMongo
from src.CommonHelpers.com import *
from src.Task.controller.task import Task
from src.GoogleAssistant.controller.handler import handle_action

url = os.environ.get('URL')
voice_app = Blueprint('voice_app', __name__, template_folder='templates')


@voice_app.route('/technodrift/voice', methods=['POST'])
def google_assistant():
    # return response
    response = results()
    print(response)
    return make_response(jsonify(response))

    # function for responses


def results():
    # build a request object
    req = request.get_json(force=True)
    print('this is request--------------------------------------------------------------------------', req,
          '===============================')
    is_login = False
    user_data = None
    try:
        action = req.get('result').get('action')
    except:
        action = req.get('queryResult').get('action')

    login_data = db['VoiceLogin'].find_one({'platform_id': req['originalDetectIntentRequest']['payload']['conversation']['conversationId']})
    if not login_data:
        is_login = False
        voice_login = {
            '_id': uuid4().hex,
            '_user': '',
            'platform_id': req['originalDetectIntentRequest']['payload']['conversation']['conversationId'],
            'is_login': False,
            'login_id': '',
            'login_time': '',
            'logout_time': '',
            'is_username_asked': False,
            'is_pin_asked': False,
            'username': '',
            'pin': '',
            'platform': 'google'
        }
        db['VoiceLogin'].insert_one(voice_login)
        is_login = False

    else:

        if action == 'input.welcome':
            if login_data['is_username_asked']:
                if login_data['username'] == '':
                    login_data['is_username_asked'] = False
            if login_data['is_pin_asked']:
                if login_data['pin'] == '':
                    login_data['is_pin_asked'] = False

        is_login = login_data['is_login']
        # if not login_data['username'] != '':
        #     is_login = False
        # else:
        #     user_data = db['User'].find_one({'platform_id': login_data['_user']})
        #     if user_data['configure']['security'] == 'private':
        #         if login_data['pin'] != '':
        #             is_login = False
        #         else:
        #             is_login = True
        #     else:
        #         is_login = True






    save_conversation(req, user_data)

    result = handle_action(action, req, is_login, user_data, login_data)
    return result


def save_conversation(req, user_data):
    db['Conversation'].insert_one({
        '_user': user_data['_id'] if user_data else '',
        'platform_id': req['originalDetectIntentRequest']['payload']['conversation']['conversationId'],
        'type': 'user',
        'message': req['queryResult']['queryText'],
        'platform': 'google',
        'created_on': int(datetime.now().timestamp())
    })
