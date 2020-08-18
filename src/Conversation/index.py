import os
import requests
from flask import Flask, Blueprint, request, jsonify, abort, make_response
from src.CommonHelpers.com import *

url = os.environ.get('URL')
conversation_app = Blueprint('conversation_app', __name__, template_folder='templates')


