import os
import requests
from flask import Flask, Blueprint, request, jsonify, abort
from src.Faqs.file_upload import Files
from src.Faqs.train import train_faq
from src.Faqs.test import TestFaq
from src.Authentication.Controller.user import Register, Login
from flask_pymongo import PyMongo

url = os.environ.get('URL')
auth_app = Blueprint('auth_app', __name__, template_folder='templates')


@auth_app.route('/', methods=['GET'])
def home():
    return jsonify(message='Welcome to Voice Assistant Service', status=True), 200


@auth_app.route('/auth/register', methods=['GET', 'POST', 'PUT', 'DELETE'])
def register():
    if request.method == 'POST':
        obj = Register(request)
        response, status = obj.post()
        return jsonify(response), status


@auth_app.route('/auth/login', methods=['GET', 'POST', 'PUT', 'DELETE'])
def login():
    if request.method == 'POST':
        obj = Login(request)
        response, status = obj.post()
        return jsonify(response), status


# @auth_app.route('/auth/profile', methods=['GET', 'PUT'])
# def profile():
#     if request.method == 'PUT':
#         obj = Profile(request)
#         response, status = obj.post()
#         return jsonify(response), status
#
#     if request.method == 'GET':
#         obj = Profile(request)
#         response, status = obj.post()
#         return jsonify(response), status