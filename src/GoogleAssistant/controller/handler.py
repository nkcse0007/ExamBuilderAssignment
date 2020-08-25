from src.GoogleAssistant.controller.components import GoogleResponse
import requests
import json
import os
from database import db
from src.Intent.controller.test import find_answer
from src.CommonHelpers.com import *

res = {
    "payload": {
        "google": {
            "expectUserResponse": True,
            "richResponse": {
                "items": [

                ]
            }
        }
    }
}


def handle_action(action, req, is_login, user_data, login_data):
    cmp_obj = GoogleResponse()
    base_cmp = cmp_obj.base_cmp()
    text = ''
    if not is_login:
        text, user_data = login_assistant(user_data, login_data, req)
    if text:
        res = {
            'type': 'question',
            'label': text
        }
        return get_response(res, base_cmp)
    bot_data = get_res_list(action, req, user_data)

    print(cmp_obj)

    # for res in bot_data['response']:
    base_cmp = get_response(bot_data, base_cmp)
    print(base_cmp)
    return base_cmp


def save_conversation(user_data, response):
    db['Conversation'].insert_one({
        '_user': user_data['_id'] if user_data else '',
        'platform_id': response['-id'],
        'type': 'bot',
        'message': response['label'],
        'platform': 'google',
        'created_on': int(datetime.now().timestamp())
    })


def login_assistant(user_data, login_data, req):
    text = ''
    user = None
    if not login_data:
        text = os.environ.get('USERNAME_QUESTION')
        db['VoiceLogin'].update_one(
            {'platform_id': req['originalDetectIntentRequest']['payload']['conversation']['conversationId']},
            {'$set': {
                'is_username_asked': True,
            }}
        )
    else:
        if login_data['is_username_asked']:
            if login_data['username'] == '':
                user = db['User'].find_one(
                    {'configure.user_name': req['queryResult']['queryText'].upper()},
                )
                if not user:
                    text = 'Your username does not match. Please try again'
                else:
                    db['VoiceLogin'].update_one(
                        {'platform_id': req['originalDetectIntentRequest']['payload']['conversation'][
                            'conversationId']},
                        {'$set': {
                            'username': req['queryResult']['queryText'].upper(),
                            '_user': user['_id'],
                        }}
                    )

        if login_data['is_pin_asked']:
            if login_data['pin'] == '':
                username = db['User'].find_one(
                    {'configure.pin': req['queryResult']['queryText']},
                )
                if not username:
                    text = 'Your pin does not match. Please try again'
                else:
                    db['User'].update_one(
                        {'_id': username['_id']},
                        {'$set': {
                            'pin': req['queryResult']['queryText'],
                        }}
                    )

        if not login_data['username'] == '':

            db['VoiceLogin'].update_one(
                {'platform_id': req['originalDetectIntentRequest']['payload']['conversation']['conversationId']},
                {'$set': {
                    'is_username_asked': True,
                }}
            )
        else:
            if login_data['_user'] != '':
                user = db['User'].find_one({'_id': login_data['_user']})
                if user['configure']['security'] == 'private':
                    if login_data['is_pin_asked']:
                        if login_data['pin'] != '':
                            if user['configure']['pin'] != req['queryResult']['queryText']:
                                text = 'Your pin does match please try again.'
                            else:
                                db['VoiceLogin'].update_one(
                                    {'platform_id': req['originalDetectIntentRequest']['payload']['conversation'][
                                        'conversationId']},
                                    {'$set': {
                                        'pin': req['queryResult']['queryText'],
                                        'is_login': True
                                    }}

                                )
                    else:
                        text = os.environ.get('PIN_QUESTION')
                        db['VoiceLogin'].update_one(
                            {'platform_id': req['originalDetectIntentRequest']['payload']['conversation'][
                                'conversationId']},
                            {'$set': {
                                'is_pin_asked': True,
                            }}
                        )
                else:
                    db['VoiceLogin'].update_one(
                        {'platform_id': req['originalDetectIntentRequest']['payload']['conversation'][
                            'conversationId']},
                        {'$set': {
                            'is_login': True,
                        }}
                    )

    return text, user


def get_res_list(action, req, user_data):
    return find_answer(user_data, req)


def get_response(res, base_cmp):
    cmp_obj = GoogleResponse()
    if res['type'] == 'statements':
        base_cmp['payload']['google']['expectUserResponse'] = True
        base_cmp['payload']['google']['richResponse']['items'].append(cmp_obj.simple(res['label']))

    elif res['type'] == 'simple_response':
        base_cmp['payload']['google']['expectUserResponse'] = True
        base_cmp['payload']['google']['richResponse']['items'].append(cmp_obj.simple_tts(res['label']))

    elif res['type'] == 'button':
        button_res = cmp_obj.button(res['label'], res['buttons'])
        return button_res
    else:
        base_cmp['payload']['google']['expectUserResponse'] = True
        base_cmp['payload']['google']['richResponse']['items'].append(cmp_obj.simple_tts(res['label']))

    return base_cmp
