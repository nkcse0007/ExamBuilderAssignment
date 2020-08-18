import os
from boto3 import exceptions
import jwt
from src.CommonHelpers import jwt_security as js
from datetime import datetime, timedelta
from uuid import uuid4
import json
from flask import Response
from database import db
from uuid import uuid4


class JwtAuth:

    def __init__(self, row_or_token):
        self.data = row_or_token

    def encode(self, payload, request):
        payload['exp']: datetime.utcnow() + timedelta(days=7)
        private_key = open('src/CommonHelpers/private.pem').read()
        user = db['User'].find_one({"_id": payload['_']})
        expires_in = int((datetime.now() + timedelta(days=30)).timestamp())
        jwt_id = uuid4().hex
        try:
            origin = request.META['HTTP_ORIGIN'].split('//')[1]
            print(request.META['HTTP_ORIGIN'].split('//')[1])
        except:
            print('EXCEPTION IN ORIGIN>>')
            # print(e)
            origin = ''

        print("================================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        encoded_jwt = jwt.encode({'userId': payload['_']}, private_key,
                                 algorithm=os.environ.get('ALGORITHM'), headers={
                'exp': expires_in,
                'aud': origin,
                'sub': user['email'],
                'iss': os.environ.get('ISSUER'),
                'jwtid': jwt_id,
                'iat': int(datetime.now().timestamp())
            })

        slz = db['JwtToken'].insert({
            '_id': uuid4().hex,
            'user': payload['_'],
            'jwtid': jwt_id,
            'expires_in': datetime.fromtimestamp(expires_in),
            'created_on': int(datetime.now().timestamp()),
            'updated_on': int(datetime.now().timestamp())
        })
        return encoded_jwt

    def decode(self):
        public_key = open('src/CommonHelpers/public.pub').read()
        decoded_jwt = jwt.decode(self.data, public_key, algorithms=os.environ.get('ALGORITHM'))
        headers = jwt.get_unverified_header(self.data)
        decoded_jwt['_'] = decoded_jwt['userId']
        return decoded_jwt, headers


def authenticate_login(fun):
    def wrap(request, *args, **kwargs):
        try:
            try:
                try:
                    token = request.META.get('HTTP_AUTHORIZATION').split()
                    if not token:
                        token = request.GET['access_token']
                        if not token:
                            token = json.loads(request.body.decode('utf-8'))['access_token']
                except:
                    try:
                        token = request.GET['access_token']
                        if not token:
                            token = json.loads(request.body.decode('utf-8'))['access_token']
                    except:
                        token = json.loads(request.body.decode('utf-8'))['access_token']

                if not token:
                    return Response({'message': 'Unauthorised user.', 'is_active': False, 'status': False},
                                    status=js.Unauthorized)

                if len(token) == 1:
                    msg = 'Invalid token header. No credentials provided.'
                    raise exceptions.AuthenticationFailed(msg)
                elif len(token) > 2:
                    msg = 'Invalid token header'
                    raise exceptions.AuthenticationFailed(msg)

                try:
                    token = token[-1]
                    if token == "null":
                        msg = 'Null token not allowed'
                        raise exceptions.AuthenticationFailed(msg)
                except UnicodeError:
                    msg = 'Invalid token header. Token string should not contain invalid characters.'
                    raise exceptions.AuthenticationFailed(msg)

                dec = JwtAuth(str(token))
                profile_id, headers = dec.decode()
            except Exception as e:
                print(e)
                return Response({'message': 'Unauthorised user', 'is_active': False, 'status': False},
                                status=js.Unauthorized)
            if db['User'].find({"id": profile_id['_']}):

                if db['User'].find({"id": profile_id['_']})['status'] == False:
                    return Response(
                        {'message': f'User has been blocked. Please contact admin.',
                         'is_active': False, 'status': False},
                        status=js.Unauthorized)
                if db['User'].find({"id": profile_id['_']})['is_deleted'] == True:
                    return Response(
                        {
                            'message': 'Unauthorised',
                            'is_active': False, 'status': False},
                        status=js.Unauthorized)

                if not db['JwtToken'].find({"jwtid": headers['jwtid']}):
                    return Response(
                        {
                            'message': 'Unauthorised',
                            'is_active': False, 'status': False},
                        status=js.Unauthorized)

                else:
                    if db['JwtToken'].find({"jwtid": headers['jwtid']})[
                        'expires_in'] < datetime.now():
                        return Response(
                            {
                                'message': f'Your account has been deleted previously. If you want to continue with same account please contact  admin.',
                                'is_active': False, 'status': False},
                            status=js.Unauthorized)
                return fun(request, *args, **kwargs)

            else:
                return Response({'message': 'Unauthorised user.', 'is_active': False, 'status': False},
                                status=js.Unauthorized)

        except Exception as e:
            return Response({'message': 'Token is required', 'status': False}, status=js.Unauthorized)

    return wrap
