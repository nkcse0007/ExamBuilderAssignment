import uuid
from flask import Response
import requests
from ip2geotools.databases.noncommercial import DbIpCity
from src.CommonHelpers.json_response import *
from src.CommonHelpers.jwt_security import *

import string
import random


def change_file_name(filename):
    extension = filename.split('.')[-1]
    return uuid.uuid4().hex + '.' + extension


def get_token(request):
    try:
        if request.headers:
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(' ')[-1]
                return token
            else:
                return Response({'message': 'Token is missing', 'status': BadRequest}, status=BadRequest)
    except Exception as e:
        return Response({'message': str(e), 'status': BadRequest}, status=BadRequest)


def get_client_ip(request):
    x_forwarded_for = request.remote_addr
    ip = x_forwarded_for.split(',')[0]
    return ip


# TODO get country from ip
def get_country_by_ip(client_ip):
    response = DbIpCity.get(client_ip, api_key='free')
    return response.country


# TODO get location from ip
def get_location(ip):
    try:
        loc = requests.request("GET", "http://ip-api.com/json/{0}".format(ip)).json()
        print(loc)
        location = loc['city'] + ', ' + loc['country'] + ', ' + loc['countryCode']
    except Exception as e:
        print(e)
        location = "unidentified"

    return location


def get_user_from_token(request):
    token = get_token(request)
    Jwt = JwtAuth(token)
    user_id, headers = Jwt.decode()[0]['_'] if '_' in Jwt.decode()[0] else 0, Jwt.decode()[1]
    return user_id


def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def alpha_id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))