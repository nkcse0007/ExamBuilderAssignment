import os
import requests
from flask import Flask, Blueprint, request, jsonify, abort
from src.CommonHelpers.com import *
from src.Configure.controller.configure import Configure

url = os.environ.get('URL')
configure_app = Blueprint('configure_app', __name__, template_folder='templates')


@configure_app.route('/configure/', methods=['GET', 'PUT'])
def configure():
    user_id = get_user_from_token(request)
    obj = Configure(request, user_id)

    if request.method == 'GET':
        response, status = obj.get()
        return jsonify(response), status

    if request.method == 'PUT':
        response, status = obj.get()
        return jsonify(response), status

