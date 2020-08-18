import os
import requests
from flask import Flask, Blueprint, request, jsonify, abort
from src.Faqs.file_upload import Files
from src.Faqs.train import train_faq
from src.Faqs.test import TestFaq
from src.Authentication.Controller.user import Register, Login
from flask_pymongo import PyMongo
from src.CommonHelpers.com import *
from src.Task.controller.task import Task

url = os.environ.get('URL')
task_app = Blueprint('task_app', __name__, template_folder='templates')


@task_app.route('/task/', methods=['GET', 'POST'])
@task_app.route('/task/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def task(task_id=None):
    user_id = get_user_from_token(request)
    print(user_id)
    obj = Task(request, user_id)

    if request.method == 'GET':
        response, status = obj.get(task_id)
        return jsonify(response), status

    if request.method == 'POST':

        response, status = obj.post()
        return jsonify(response), status

    if request.method == 'PUT':
        response, status = obj.put(task_id)
        return jsonify(response), status

    if request.method == 'DELETE':
        response, status = obj.delete(task_id)
        return jsonify(response), status

