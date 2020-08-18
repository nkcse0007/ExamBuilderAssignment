from database import db
from src.CommonHelpers.com import *
from src.CommonHelpers.json_response import *
from src.CommonHelpers.jwt_security import *
from src.CommonHelpers.validations import *
import hashlib
from uuid import uuid4


class Register:
    def __init__(self, request):
        self.request = request
        self.input_data = json.loads(request.data)

    def post(self):
        if not self.input_data:
            return {'message': 'data is missing.', 'status': BadRequest}, 400
        elif 'name' not in self.input_data or self.input_data['name'] == '':
            return {'message': 'name is missing.', 'status': BadRequest}, 400
        elif 'email' not in self.input_data or self.input_data['email'] == '':
            return {'message': 'email is missing.', 'status': BadRequest}, 400
        elif 'phone' not in self.input_data or self.input_data['phone'] == '':
            return {'message': 'phone is missing.', 'status': BadRequest}, 400
        elif 'password' not in self.input_data or self.input_data['password'] == '':
            return {'message': 'password is missing.', 'status': BadRequest}, 400
        elif db['User'].find({"email": self.input_data['email'].lower()}).count():
            return {'message': 'You already have your account.Please Login.', 'status': BadRequest}, 400
        elif isValidEmail(self.input_data['email']) is not True:
            return {'message': 'Invalid email.', 'status': BadRequest}, 400
        elif len(self.input_data['password']) < 6:
            return {
                       'message': 'invalid password. password must be 6 or greater then 6 characters. ',
                       'status': BadRequest}, 400
        else:
            self.input_data['password'] = hashlib.sha512(self.input_data['password'].encode()).hexdigest()
            ip = get_client_ip(self.request)
            location = get_location(ip)
            self.input_data['_id'] = uuid4().hex
            self.input_data['email'] = self.input_data['email'].lower()
            self.input_data['location'] = location
            self.input_data['is_verified'] = True
            self.input_data['is_deleted'] = False
            self.input_data['created_on'] = datetime.now()
            self.input_data['is_deleted'] = datetime.now()
            self.input_data['configure'] = {
                'user_name': alpha_id_generator(),
                'pin': id_generator(),
                'security': 'public'
            }

            profile = db['User'].insert(self.input_data)




            if not profile:
                return {'status': BadRequest, 'message': 'something went wrong'}, 400
            user = db['User'].find_one({"email": self.input_data['email']})
            Jwt = JwtAuth('VoiceAssistant')
            token = Jwt.encode(
                {'_': str(user['_id']), '___': user['email'], '____': user['name']}, self.request)
            return {'status': Created,
                    'data': {'email': user['email'], 'phone': user['phone'], 'token': token.decode()},
                    'message': 'Registration successful. Please check your email to activate your account.'}, 200


class Login:
    def __init__(self, request):
        self.request = request
        self.input_data = json.loads(request.data)

    def post(self):
        if not self.input_data:
            return {'message': 'data is missing.', 'status': BadRequest}, 400
        elif 'email' not in self.input_data or self.input_data['email'] == '':
            return {'message': 'email is missing.', 'status': BadRequest}, 400
        elif 'password' not in self.input_data or self.input_data['password'] == '':
            return {'message': 'password is missing.', 'status': BadRequest}, 400
        elif not db['User'].find({"email": self.input_data['email'].lower()}).count():
            return {'message': 'You do not have any account.Please Register first.', 'status': BadRequest}, 400
        else:
            self.input_data['password'] = hashlib.sha512(self.input_data['password'].encode()).hexdigest()

            user = db['User'].find_one({"email": self.input_data['email']})
            if self.input_data['password'] != user['password']:
                return {'message': 'Wrong password, Please try again.', 'status': BadRequest}, 400
            Jwt = JwtAuth('VoiceAssistant')
            token = Jwt.encode(
                {'_': str(user['_id']), '___': user['email'], '____': user['name']}, self.request)
            return {'status': OK,
                    'message': 'Login successful.',
                    'data': {'email': user['email'], 'phone': user['phone'], 'token': token.decode()}}, 200
