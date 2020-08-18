import os
from flask import Blueprint, request, jsonify
from src.Intent.controller.train import train_intents
from src.Intent.controller.test import test_intent
from src.CommonHelpers.com import *

url = os.environ.get('URL')
intent_app = Blueprint('intent_route', __name__, template_folder='templates')


@intent_app.route('/nlp/intent/train', methods=['GET'])
def train():
    user_id = get_user_from_token(request)
    response, status = train_intents(user_id)
    return jsonify(response), status


@intent_app.route('/nlp/intent/test', methods=['POST'])
def test():
    user_id = get_user_from_token(request)
    response, status = test_intent(user_id)
    return jsonify(response), status
